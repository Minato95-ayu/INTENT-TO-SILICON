import os

files_to_write = {
    "official_packages/aayu-auth/main.aayu": """app AayuAuth

action login(username, password)
    return auth.login(username, password)
end

action register(username, password)
    return auth.register(username, password)
end
""",
    "official_packages/aayu-crypto/main.aayu": """app AayuCrypto

action hash(data)
    return crypto::sha256(data)
end
""",
    "official_packages/aayu-dataframe/main.aayu": """app AayuDataframe

action loadCSV(path)
    return df_read_csv(path)
end
""",
    "official_packages/aayu-datetime/main.aayu": """app AayuDatetime

action now()
    return time::now()
end
""",
    "official_packages/aayu-email/main.aayu": """app AayuEmail

action sendEmail(to, subject, body)
    print("Email Sent to: ")
    print(to)
    return 1
end
""",
    "official_packages/aayu-fs/main.aayu": """app AayuFS

action readFile(path)
    return file::read(path)
end

action writeFile(path, content)
    return file::write(path, content)
end
""",
    "official_packages/aayu-gemini/main.aayu": """app AayuGemini

action generateContent(prompt)
    return ai::generate(prompt)
end
""",
    "official_packages/aayu-http/main.aayu": """app AayuHttp

action getReq(url)
    return http::get(url)
end

action postReq(url, data)
    return http::post(url, data)
end
""",
    "official_packages/aayu-json/main.aayu": """app AayuJson

action parse(data)
    return json::parse(data)
end

action stringify(data)
    return json::stringify(data)
end
""",
    "official_packages/aayu-math/main.aayu": """app AayuMath

action add(a, b)
    return a + b
end

action abs(v)
    return math::abs(v)
end
""",
    "official_packages/aayu-ml/main.aayu": """app AayuML

action trainKMeans(data, k)
    return ml::kmeans_fit(data, k, 100)
end
""",
    "official_packages/aayu-openai/main.aayu": """app AayuOpenAI

action generateText(prompt)
    return ai::generate(prompt)
end
""",
    "official_packages/aayu-rag/main.aayu": """app AayuRag

action queryDocument(query)
    print("RAG query: ")
    print(query)
    return "Result"
end
""",
    "official_packages/aayu-upload/main.aayu": """app AayuUpload

action uploadFile(file)
    print("Uploading: ")
    print(file)
    return 1
end
""",
    "official_packages/aayu-vision/main.aayu": """app AayuVision

action analyzeImage(image_path)
    print("Analyzing vision for: ")
    print(image_path)
    return "Object detected"
end
"""
}

for path, content in files_to_write.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Packages updated!")
