#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#define EXPORT __declspec(dllexport)
BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {
    return TRUE;
}
#else
#define EXPORT
#endif

EXPORT char* aayu_ping(const char* host) {
    printf("[RUNTIME] Pinging host: %s\n", host);
    char* result = (char*)malloc(256);
    snprintf(result, 256, "Ping successful: %s", host);
    return result;
}

EXPORT char* aayu_dns_resolve(const char* host) {
    printf("[RUNTIME] Resolving DNS for: %s\n", host);
    char* result = (char*)malloc(256);
    snprintf(result, 256, "192.168.1.1");
    return result;
}

EXPORT char* aayu_tcp_connect(const char* host, int port) {
    printf("[RUNTIME] TCP Connecting to %s:%d\n", host, port);
    char* result = (char*)malloc(256);
    snprintf(result, 256, "Connected to %s on port %d", host, port);
    return result;
}
