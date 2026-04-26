// Minimal helpers for the net/final-style labs.
// These mimic the small API used by the exercises, but intentionally avoid
// setuid/daemon behavior so they can run as an unprivileged user locally.

#define _GNU_SOURCE

#include <arpa/inet.h>
#include <errno.h>
#include <err.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

static int g_listen_fd = -1;

static void cleanup(void) {
  if (g_listen_fd != -1) {
    close(g_listen_fd);
    g_listen_fd = -1;
  }
}

void background_process(const char *name, int uid, int gid) {
  (void)name;
  (void)uid;
  (void)gid;
  // Keep behavior simple for local use:
  // - no daemon(), no setuid(), no chdir()
  // - still ensure the listener gets cleaned up on exit
  atexit(cleanup);
  signal(SIGPIPE, SIG_IGN);
}

int serve_forever(int port) {
  int fd;
  int one = 1;
  struct sockaddr_in sin;

  fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd == -1)
    err(1, "socket");

  if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one)) == -1)
    err(1, "setsockopt");

  memset(&sin, 0, sizeof(sin));
  sin.sin_family = AF_INET;
  sin.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
  sin.sin_port = htons((unsigned short)port);

  if (bind(fd, (struct sockaddr *)&sin, sizeof(sin)) == -1)
    err(1, "bind");

  if (listen(fd, 1) == -1)
    err(1, "listen");

  g_listen_fd = fd;

  // Accept a single client and return it.
  int cfd = accept(fd, NULL, NULL);
  if (cfd == -1)
    err(1, "accept");

  // Close listener after first connection to keep behavior deterministic.
  close(fd);
  g_listen_fd = -1;
  return cfd;
}

void set_io(int fd) {
  if (dup2(fd, 0) == -1)
    err(1, "dup2 stdin");
  if (dup2(fd, 1) == -1)
    err(1, "dup2 stdout");
  if (dup2(fd, 2) == -1)
    err(1, "dup2 stderr");
  if (fd > 2)
    close(fd);
}

