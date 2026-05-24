const keywordsInput = document.getElementById("keywords");
const output = document.getElementById("output");
const statusEl = document.getElementById("status");

async function generateCopy() {
  const keywords = keywordsInput.value.trim();
  if (!keywords) {
    statusEl.textContent = "请先输入关键词";
    return;
  }

  statusEl.textContent = "生成中...";
  const res = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ keywords }),
  });

  const data = await res.json();
  if (!res.ok) {
    statusEl.textContent = data.error || "生成失败，请重试";
    return;
  }

  output.value = data.content;
  statusEl.textContent = "生成完成";
}

async function copyText() {
  const text = output.value.trim();
  if (!text) {
    statusEl.textContent = "没有可复制内容";
    return;
  }
  await navigator.clipboard.writeText(text);
  statusEl.textContent = "已复制到剪贴板";
}

document.getElementById("generateBtn").addEventListener("click", generateCopy);
document.getElementById("copyBtn").addEventListener("click", copyText);
