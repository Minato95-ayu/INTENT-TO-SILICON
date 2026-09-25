"use client";
import React, { useEffect, useState } from "react";

export default function DownloadTerminal() {
  const [os, setOs] = useState("windows");

  useEffect(() => {
    const userAgent = window.navigator.userAgent.toLowerCase();
    if (userAgent.includes("android") || userAgent.includes("iphone") || userAgent.includes("ipad")) {
      setOs("mobile");
    } else if (userAgent.includes("mac")) {
      setOs("mac");
    } else if (userAgent.includes("linux")) {
      setOs("linux");
    } else {
      setOs("windows");
    }
  }, []);

  if (os === "mobile") {
    return (
      <div className="bg-black border border-white/10 rounded-xl p-6 max-w-lg mx-auto text-left font-mono text-sm mb-10 space-y-3">
        <div className="flex items-center gap-3">
          <span className="text-zinc-600 select-none">$</span>
          <span className="text-zinc-400"># 1. Mobile Device Detected!</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-zinc-600 select-none">$</span>
          <span className="text-blue-400"># AAYU requires a Desktop OS to compile natively.</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-zinc-600 select-none">$</span>
          <span className="text-green-400"># Please visit this site on Windows, Mac, or Linux!</span>
        </div>
        <div className="border-t border-white/5 pt-3 mt-3">
          <span className="text-zinc-500">Note: You can run AAYU on Android via Termux + Python.</span>
        </div>
      </div>
    );
  }

  const isMac = os === "mac";
  const isLinux = os === "linux";
  const binary = isMac ? "aayu-macos.pkg" : isLinux ? "aayu-linux.tar.gz" : "aayu.exe";
  const runCmd = isMac || isLinux ? "./aayu main.aayu" : "./aayu.exe main.aayu";

  return (
    <div className="bg-black border border-white/10 rounded-xl p-6 max-w-lg mx-auto text-left font-mono text-sm mb-10 space-y-3">
      <div className="flex items-center gap-3">
        <span className="text-zinc-600 select-none">$</span>
        <span className="text-zinc-400"># 1. Download the standalone compiler for {os.toUpperCase()}</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-zinc-600 select-none">$</span>
        <span className="text-green-400 break-all">curl -LO https://aayu.run/releases/latest/{binary}</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-zinc-600 select-none">$</span>
        <span className="text-blue-400">{runCmd}</span>
      </div>
      <div className="border-t border-white/5 pt-3 mt-3">
        <span className="text-emerald-400">✓ Compiled to Native machine code in 12ms</span>
      </div>
      <div>
        <span className="text-emerald-400">▶ Execution output: Hello from AAYU</span>
      </div>
    </div>
  );
}
