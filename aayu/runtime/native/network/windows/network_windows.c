#include "../../runtime.h"

#ifdef _WIN32

#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
#include <icmpapi.h>
#include <stdio.h>
#include <string.h>

#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "iphlpapi.lib")

// Initialize Winsock if not already done.
static int ensure_winsock_init(void) {
    static int initialized = 0;
    if (!initialized) {
        WSADATA wsaData;
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
            return -1;
        }
        initialized = 1;
    }
    return 0;
}

AAYU_EXPORT AayuPingResult aayu_ping(const char* host) {
    AayuPingResult result;
    memset(&result, 0, sizeof(result));
    result.success = 0;
    result.latency_ms = -1;
    
    if (ensure_winsock_init() != 0) return result;

    // Resolve hostname to IP first.
    struct addrinfo hints, *res;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET; // Force IPv4 for ICMP ease
    hints.ai_socktype = SOCK_STREAM;
    
    if (getaddrinfo(host, NULL, &hints, &res) != 0) {
        return result;
    }

    struct sockaddr_in *ipv4 = (struct sockaddr_in *)res->ai_addr;
    void *addr = &(ipv4->sin_addr);
    inet_ntop(AF_INET, addr, result.ip, sizeof(result.ip));

    IPAddr ip = ipv4->sin_addr.S_un.S_addr;
    freeaddrinfo(res);

    HANDLE hIcmpFile = IcmpCreateFile();
    if (hIcmpFile == INVALID_HANDLE_VALUE) {
        return result;
    }

    char SendData[32] = "AAYU Ping Test";
    DWORD ReplySize = sizeof(ICMP_ECHO_REPLY) + sizeof(SendData) + 8;
    LPVOID ReplyBuffer = malloc(ReplySize);
    if (!ReplyBuffer) {
        IcmpCloseHandle(hIcmpFile);
        return result;
    }

    DWORD dwRetVal = IcmpSendEcho(hIcmpFile, ip, SendData, sizeof(SendData),
                                  NULL, ReplyBuffer, ReplySize, 1000);

    if (dwRetVal != 0) {
        PICMP_ECHO_REPLY pEchoReply = (PICMP_ECHO_REPLY)ReplyBuffer;
        result.success = 1;
        result.latency_ms = pEchoReply->RoundTripTime;
    }

    free(ReplyBuffer);
    IcmpCloseHandle(hIcmpFile);

    return result;
}

AAYU_EXPORT AayuDNSResult aayu_dns_resolve(const char* host) {
    AayuDNSResult result;
    memset(&result, 0, sizeof(result));
    result.success = 0;
    
    if (ensure_winsock_init() != 0) return result;

    struct addrinfo hints, *res;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if (getaddrinfo(host, NULL, &hints, &res) == 0) {
        void *addr;
        if (res->ai_family == AF_INET) { // IPv4
            struct sockaddr_in *ipv4 = (struct sockaddr_in *)res->ai_addr;
            addr = &(ipv4->sin_addr);
            inet_ntop(AF_INET, addr, result.ip, sizeof(result.ip));
        } else { // IPv6
            struct sockaddr_in6 *ipv6 = (struct sockaddr_in6 *)res->ai_addr;
            addr = &(ipv6->sin6_addr);
            inet_ntop(AF_INET6, addr, result.ip, sizeof(result.ip));
        }
        result.success = 1;
        freeaddrinfo(res);
    }

    return result;
}

AAYU_EXPORT AayuTCPResult aayu_tcp_connect(const char* host, int32_t port) {
    AayuTCPResult result;
    memset(&result, 0, sizeof(result));
    result.success = 0;
    result.latency_ms = -1;

    if (ensure_winsock_init() != 0) return result;

    char port_str[16];
    sprintf(port_str, "%d", port);

    struct addrinfo hints, *res;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    if (getaddrinfo(host, port_str, &hints, &res) != 0) {
        return result;
    }

    SOCKET ConnectSocket = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
    if (ConnectSocket == INVALID_SOCKET) {
        freeaddrinfo(res);
        return result;
    }

    // Time the connection
    DWORD start = GetTickCount();
    if (connect(ConnectSocket, res->ai_addr, (int)res->ai_addrlen) != SOCKET_ERROR) {
        DWORD end = GetTickCount();
        result.success = 1;
        result.latency_ms = (int32_t)(end - start);
    }

    closesocket(ConnectSocket);
    freeaddrinfo(res);

    return result;
}

#endif // _WIN32
