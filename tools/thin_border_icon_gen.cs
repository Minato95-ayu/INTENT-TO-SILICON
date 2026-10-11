using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;

class Program
{
    static void Main()
    {
        string inputJpg = @"C:\Users\Miinato\.gemini\antigravity\brain\4de249f6-0127-4acc-a01f-e1989fb35ecc\aayu_official_emoji_1791725591327.jpg";
        if (!File.Exists(inputJpg))
        {
            inputJpg = @"C:\Users\Miinato\.gemini\antigravity\brain\4de249f6-0127-4acc-a01f-e1989fb35ecc\.user_uploaded\media_1791721628008_54b3ec40.jpg";
        }

        Console.WriteLine("Loading master artwork from: " + inputJpg);
        using (Bitmap src = new Bitmap(inputJpg))
        {
            int w = src.Width;
            int h = src.Height;

            // Step 1: Crop tightly to the letter 'A'
            // We want to discard the thick outer border and keep the rich inner brain and circuit
            // Bounding box scan of non-black pixels
            BitmapData srcData = src.LockBits(new Rectangle(0, 0, w, h), ImageLockMode.ReadOnly, PixelFormat.Format24bppRgb);
            byte[] srcBytes = new byte[srcData.Stride * h];
            System.Runtime.InteropServices.Marshal.Copy(srcData.Scan0, srcBytes, 0, srcBytes.Length);
            src.UnlockBits(srcData);

            Func<int, int, int> getBrightness = (x, y) => {
                int idx = y * srcData.Stride + x * 3;
                return (srcBytes[idx] + srcBytes[idx + 1] + srcBytes[idx + 2]) / 3;
            };

            // BFS Flood Fill to remove background outside the 'A'
            bool[,] isBg = new bool[w, h];
            Queue<Point> q = new Queue<Point>();

            int bgThreshold = 18;
            for (int x = 0; x < w; x++) {
                if (getBrightness(x, 0) <= bgThreshold) { isBg[x, 0] = true; q.Enqueue(new Point(x, 0)); }
                if (getBrightness(x, h - 1) <= bgThreshold) { isBg[x, h - 1] = true; q.Enqueue(new Point(x, h - 1)); }
            }
            for (int y = 0; y < h; y++) {
                if (getBrightness(0, y) <= bgThreshold) { isBg[0, y] = true; q.Enqueue(new Point(0, y)); }
                if (getBrightness(w - 1, y) <= bgThreshold) { isBg[w - 1, y] = true; q.Enqueue(new Point(w - 1, y)); }
            }

            // Inner triangle eye (around 512, 500)
            if (getBrightness(512, 500) <= bgThreshold) {
                isBg[512, 500] = true;
                q.Enqueue(new Point(512, 500));
            }

            int[] dx = { 0, 0, 1, -1 };
            int[] dy = { 1, -1, 0, 0 };

            while (q.Count > 0)
            {
                Point pt = q.Dequeue();
                for (int i = 0; i < 4; i++)
                {
                    int nx = pt.X + dx[i];
                    int ny = pt.Y + dy[i];
                    if (nx >= 0 && nx < w && ny >= 0 && ny < h && !isBg[nx, ny])
                    {
                        if (getBrightness(nx, ny) <= bgThreshold)
                        {
                            isBg[nx, ny] = true;
                            q.Enqueue(new Point(nx, ny));
                        }
                    }
                }
            }

            // Find tight bounding box of the actual letter 'A'
            int minX = w, maxX = 0, minY = h, maxY = 0;
            for (int y = 0; y < h; y++)
            {
                for (int x = 0; x < w; x++)
                {
                    if (!isBg[x, y] && getBrightness(x, y) > 25)
                    {
                        if (x < minX) minX = x;
                        if (x > maxX) maxX = x;
                        if (y < minY) minY = y;
                        if (y > maxY) maxY = y;
                    }
                }
            }

            Console.WriteLine(string.Format("Glyph bounds: minX={0}, maxX={1}, minY={2}, maxY={3}", minX, maxX, minY, maxY));

            // Extract the isolated glyph into transparent 32bpp bitmap
            int cropW = maxX - minX + 1;
            int cropH = maxY - minY + 1;
            Bitmap glyph = new Bitmap(cropW, cropH, PixelFormat.Format32bppArgb);

            BitmapData glyphData = glyph.LockBits(new Rectangle(0, 0, cropW, cropH), ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb);
            byte[] glyphBytes = new byte[glyphData.Stride * cropH];

            for (int y = 0; y < cropH; y++)
            {
                int origY = y + minY;
                for (int x = 0; x < cropW; x++)
                {
                    int origX = x + minX;
                    int srcIdx = origY * srcData.Stride + origX * 3;
                    int dstIdx = y * glyphData.Stride + x * 4;

                    byte b = srcBytes[srcIdx];
                    byte g = srcBytes[srcIdx + 1];
                    byte r = srcBytes[srcIdx + 2];

                    if (isBg[origX, origY])
                    {
                        glyphBytes[dstIdx] = 0;
                        glyphBytes[dstIdx + 1] = 0;
                        glyphBytes[dstIdx + 2] = 0;
                        glyphBytes[dstIdx + 3] = 0;
                    }
                    else
                    {
                        int br = (r + g + b) / 3;
                        byte a = 255;
                        if (br < 35) a = (byte)(br * 255 / 35);

                        glyphBytes[dstIdx] = b;
                        glyphBytes[dstIdx + 1] = g;
                        glyphBytes[dstIdx + 2] = r;
                        glyphBytes[dstIdx + 3] = a;
                    }
                }
            }
            System.Runtime.InteropServices.Marshal.Copy(glyphBytes, 0, glyphData.Scan0, glyphBytes.Length);
            glyph.UnlockBits(glyphData);

            // Step 2: Render crisp multi-scale icons with THIN BORDER and MAXIMUM ARTWORK SIZE
            string iconDir = @"D:\INTENT-TO-SILICON\vscode-aayu\icons";
            string extDir = @"C:\Users\Miinato\.vscode\extensions\ayushghritkaushik.aayu-1.2.0\icons";
            string emojiDir = @"D:\INTENT-TO-SILICON\assets\emojis";
            string assetDir = @"D:\INTENT-TO-SILICON\assets\icons";

            Directory.CreateDirectory(iconDir);
            Directory.CreateDirectory(extDir);
            Directory.CreateDirectory(emojiDir);
            Directory.CreateDirectory(assetDir);

            int[] sizes = { 128, 64, 32, 16 };
            foreach (int sz in sizes)
            {
                Bitmap dark = RenderIcon(glyph, sz, true);
                Bitmap light = RenderIcon(glyph, sz, false);

                dark.Save(Path.Combine(iconDir, "aayu-dark-" + sz + ".png"), ImageFormat.Png);
                light.Save(Path.Combine(iconDir, "aayu-light-" + sz + ".png"), ImageFormat.Png);
                dark.Save(Path.Combine(extDir, "aayu-dark-" + sz + ".png"), ImageFormat.Png);
                light.Save(Path.Combine(extDir, "aayu-light-" + sz + ".png"), ImageFormat.Png);

                if (sz == 128)
                {
                    dark.Save(Path.Combine(iconDir, "aayu-dark.png"), ImageFormat.Png);
                    light.Save(Path.Combine(iconDir, "aayu-light.png"), ImageFormat.Png);
                    dark.Save(Path.Combine(extDir, "aayu-dark.png"), ImageFormat.Png);
                    light.Save(Path.Combine(extDir, "aayu-light.png"), ImageFormat.Png);
                    dark.Save(Path.Combine(assetDir, "aayu-dark.png"), ImageFormat.Png);
                    light.Save(Path.Combine(assetDir, "aayu-light.png"), ImageFormat.Png);
                    dark.Save(Path.Combine(emojiDir, "aayu_128.png"), ImageFormat.Png);
                    dark.Save(@"D:\INTENT-TO-SILICON\vscode-aayu\icon.png", ImageFormat.Png);
                    dark.Save(@"C:\Users\Miinato\.vscode\extensions\ayushghritkaushik.aayu-1.2.0\icon.png", ImageFormat.Png);
                }
                if (sz == 64) dark.Save(Path.Combine(emojiDir, "aayu_64.png"), ImageFormat.Png);
                if (sz == 32) dark.Save(Path.Combine(emojiDir, "aayu_32.png"), ImageFormat.Png);

                dark.Dispose();
                light.Dispose();
            }

            glyph.Dispose();
            Console.WriteLine("All thin-border icons successfully generated and saved!");
        }
    }

    static Bitmap RenderIcon(Bitmap masterGlyph, int sz, bool isDark)
    {
        Bitmap res = new Bitmap(sz, sz, PixelFormat.Format32bppArgb);
        using (Graphics g = Graphics.FromImage(res))
        {
            g.SmoothingMode = SmoothingMode.HighQuality;
            g.InterpolationMode = InterpolationMode.HighQualityBicubic;
            g.PixelOffsetMode = PixelOffsetMode.HighQuality;
            g.CompositingQuality = CompositingQuality.HighQuality;

            // Full bleed fill: padding is minimal (only 1px or 0px for small sizes)
            // This maximizes the brain & silicon details to 96% of the icon!
            int pad = sz <= 24 ? 0 : 2;
            int drawW = sz - (pad * 2);
            int drawH = sz - (pad * 2);

            g.DrawImage(masterGlyph, pad, pad, drawW, drawH);

            // Add ultra-thin 1px crisp outline border around the letter A
            // Left: Crisp luminous white
            // Right: Crisp glowing neon red
            float s = sz / 128.0f;
            float penW = Math.Max(1.0f, 1.4f * s);

            Color colL = isDark ? Color.FromArgb(240, 255, 255, 255) : Color.FromArgb(240, 30, 41, 59);
            Color colR = isDark ? Color.FromArgb(240, 255, 30, 60) : Color.FromArgb(240, 220, 38, 38);

            using (Pen pL = new Pen(colL, penW) { StartCap = LineCap.Round, EndCap = LineCap.Round, LineJoin = LineJoin.Round })
            using (Pen pR = new Pen(colR, penW) { StartCap = LineCap.Round, EndCap = LineCap.Round, LineJoin = LineJoin.Round })
            {
                PointF[] lPts = new PointF[] {
                    new PointF(sz * 0.5f, pad + 1),
                    new PointF(pad + 1, sz - pad - 1),
                    new PointF(sz * 0.32f, sz - pad - 1),
                    new PointF(sz * 0.40f, sz * 0.78f)
                };
                g.DrawLines(pL, lPts);

                PointF[] rPts = new PointF[] {
                    new PointF(sz * 0.5f, pad + 1),
                    new PointF(sz - pad - 1, sz - pad - 1),
                    new PointF(sz * 0.68f, sz - pad - 1),
                    new PointF(sz * 0.60f, sz * 0.78f)
                };
                g.DrawLines(pR, rPts);
            }
        }

        // Apply vibrancy & detail boost
        BitmapData bd = res.LockBits(new Rectangle(0, 0, sz, sz), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
        byte[] bytes = new byte[bd.Stride * sz];
        System.Runtime.InteropServices.Marshal.Copy(bd.Scan0, bytes, 0, bytes.Length);

        for (int i = 0; i < bytes.Length; i += 4)
        {
            byte b = bytes[i];
            byte g = bytes[i + 1];
            byte r = bytes[i + 2];
            byte a = bytes[i + 3];

            if (a > 10)
            {
                // Circuit side: boost saturated neon electric red
                if (r > g + 15)
                {
                    bytes[i + 2] = (byte)Math.Min(255, (int)(r * 1.35f + 30));
                    bytes[i + 1] = (byte)Math.Max(0, (int)(g * 0.85f));
                    bytes[i] = (byte)Math.Max(0, (int)(b * 0.85f));
                }
                // Brain side: boost bright white highlights
                else if (r > 90 && g > 90 && b > 90)
                {
                    if (isDark)
                    {
                        bytes[i + 2] = (byte)Math.Min(255, (int)(r * 1.3f + 25));
                        bytes[i + 1] = (byte)Math.Min(255, (int)(g * 1.3f + 25));
                        bytes[i] = (byte)Math.Min(255, (int)(b * 1.3f + 25));
                    }
                    else
                    {
                        // In light mode, maintain high contrast
                        bytes[i + 2] = (byte)(r * 0.68f);
                        bytes[i + 1] = (byte)(g * 0.68f);
                        bytes[i] = (byte)(b * 0.68f);
                    }
                }
            }
        }

        System.Runtime.InteropServices.Marshal.Copy(bytes, 0, bd.Scan0, bytes.Length);
        res.UnlockBits(bd);
        return res;
    }
}
