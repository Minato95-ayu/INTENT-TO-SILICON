fn main() {
    if std::env::var("CARGO_CFG_TARGET_OS").unwrap() == "windows" {
        let mut res = winres::WindowsResource::new();
        res.set_icon("../aayu-icon.ico");
        res.set_language(0x0409);
        res.set("FileDescription", "AAYU Intent-to-Silicon Programming Language Engine");
        res.set("ProductName", "AAYU Programming Language");
        res.set("CompanyName", "Ayush Ghrit Kaushik (AAYU Foundation)");
        res.set("LegalCopyright", "Copyright (C) 2026 Ayush Ghrit Kaushik. All rights reserved.");
        res.set("OriginalFilename", "aayu.exe");
        res.set("InternalName", "aayu");
        res.set("FileVersion", "1.2.0.0");
        res.set("ProductVersion", "1.2.0.0");
        res.set_manifest(r#"
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="asInvoker" uiAccess="false" />
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
"#);
        res.compile().unwrap();

        let out_dir = std::env::var("OUT_DIR").unwrap();
        let obj_path = format!("{}/resource.o", out_dir);
        if std::path::Path::new(&obj_path).exists() {
            println!("cargo:rustc-link-arg={}", obj_path);
        }
    }
}
