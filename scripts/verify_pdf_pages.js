const fs = require('fs');
const zlib = require('zlib');

const buf = fs.readFileSync('test_out.pdf');
const str = buf.toString('latin1');

// Match all Page objects
const pageRegex = /(\d+)\s+0\s+obj\s*<<\s*\/Type\s*\/Page\b([\s\S]*?)>>\s*endobj/g;
let m;
const pages = [];
while ((m = pageRegex.exec(str)) !== null) {
  const objId = m[1];
  const dict = m[2];
  const cMatch = dict.match(/\/Contents\s+(\d+)\s+0\s+R/);
  if (cMatch) {
    pages.push({ pageNum: pages.length + 1, objId, contentsId: cMatch[1] });
  }
}

console.log('Total PDF Pages found:', pages.length);

pages.slice(0, 6).forEach(p => {
  const startMarker = p.contentsId + ' 0 obj';
  const startIdx = str.indexOf(startMarker);
  if (startIdx === -1) {
    console.log('Page ' + p.pageNum + ': obj ' + p.contentsId + ' not found');
    return;
  }
  const streamIdx = str.indexOf('stream', startIdx);
  const endStreamIdx = str.indexOf('endstream', streamIdx);
  let rawStream = buf.subarray(streamIdx + 6, endStreamIdx);
  // strip leading CR/LF
  if (rawStream[0] === 0x0d && rawStream[1] === 0x0a) rawStream = rawStream.subarray(2);
  else if (rawStream[0] === 0x0a || rawStream[0] === 0x0d) rawStream = rawStream.subarray(1);

  try {
    const decomp = zlib.inflateSync(rawStream);
    console.log('Page ' + p.pageNum + ' (Contents ' + p.contentsId + ') decompressed size: ' + decomp.length + ' bytes');
  } catch (err) {
    console.log('Page ' + p.pageNum + ' inflate error: ' + err.message);
  }
});
