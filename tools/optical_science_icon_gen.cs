using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;

class OpticalScienceIconGen
{
    static void Main()
    {
        Console.WriteLine("Generating Optically-Tuned Scientific HD AAYU Icons...");

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
            Bitmap dark = RenderOpticallyEngineeredIcon(sz, true);
            Bitmap light = RenderOpticallyEngineeredIcon(sz, false);

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
                dark.Save(Path.Combine(assetDir, "aayu-light.png"), ImageFormat.Png);
                dark.Save(Path.Combine(emojiDir, "aayu_128.png"), ImageFormat.Png);
                dark.Save(@"D:\INTENT-TO-SILICON\vscode-aayu\icon.png", ImageFormat.Png);
                dark.Save(@"C:\Users\Miinato\.vscode\extensions\ayushghritkaushik.aayu-1.2.0\icon.png", ImageFormat.Png);
            }
            if (sz == 64) dark.Save(Path.Combine(emojiDir, "aayu_64.png"), ImageFormat.Png);
            if (sz == 32) dark.Save(Path.Combine(emojiDir, "aayu_32.png"), ImageFormat.Png);

            dark.Dispose();
            light.Dispose();
        }

        // Generate Pure Vector SVGs optimized for sub-pixel rendering
        string svgDark = GenerateVectorSvg(true);
        string svgLight = GenerateVectorSvg(false);

        File.WriteAllText(Path.Combine(iconDir, "aayu-dark.svg"), svgDark);
        File.WriteAllText(Path.Combine(iconDir, "aayu-light.svg"), svgLight);
        File.WriteAllText(Path.Combine(extDir, "aayu-dark.svg"), svgDark);
        File.WriteAllText(Path.Combine(extDir, "aayu-light.svg"), svgLight);

        Console.WriteLine("All Optically-Engineered Scientific Icons successfully generated!");
    }

    static Bitmap RenderOpticallyEngineeredIcon(int sz, bool isDark)
    {
        Bitmap bmp = new Bitmap(sz, sz, PixelFormat.Format32bppArgb);
        using (Graphics g = Graphics.FromImage(bmp))
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.InterpolationMode = InterpolationMode.HighQualityBicubic;
            g.PixelOffsetMode = PixelOffsetMode.HighQuality;

            float s = sz / 16.0f; // 16x16 reference grid

            // 1. HARD BLACK SUBSTRATE / BASE FOR THE LETTER 'A'
            // This gives the brain crevices and circuit board a deep pure black backdrop!
            PointF[] aContour = new PointF[] {
                new PointF(8f * s, 0.5f * s),
                new PointF(15.5f * s, 15.5f * s),
                new PointF(11.2f * s, 15.5f * s),
                new PointF(9.8f * s, 12.5f * s),
                new PointF(6.2f * s, 12.5f * s),
                new PointF(4.8f * s, 15.5f * s),
                new PointF(0.5f * s, 15.5f * s)
            };
            using (Brush bBlack = new SolidBrush(Color.FromArgb(255, 4, 4, 8)))
            {
                g.FillPolygon(bBlack, aContour);
            }

            // Central Eye Cutout (Transparent Triangle)
            PointF[] eyeTriangle = new PointF[] {
                new PointF(8f * s, 5.2f * s),
                new PointF(6.4f * s, 9.8f * s),
                new PointF(9.6f * s, 9.8f * s)
            };

            // 2. LEFT HALF: HUMAN BRAIN (OPTICALLY TUNED LUMINOUS SILVER/WHITE 3D LOBES)
            // Colors: Pure White highlight, Platinum body, Hard Black fissure shadows
            Color brainMain = isDark ? Color.FromArgb(255, 230, 238, 248) : Color.FromArgb(255, 60, 75, 95);
            Color brainHighlight = isDark ? Color.FromArgb(255, 255, 255, 255) : Color.FromArgb(255, 140, 160, 185);

            float brainW = Math.Max(1.4f, 1.8f * s);
            float brainHiW = Math.Max(0.8f, 0.9f * s);

            using (Pen pBr = new Pen(brainMain, brainW) { StartCap = LineCap.Round, EndCap = LineCap.Round, LineJoin = LineJoin.Round })
            using (Pen pHi = new Pen(brainHighlight, brainHiW) { StartCap = LineCap.Round, EndCap = LineCap.Round, LineJoin = LineJoin.Round })
            {
                // Superior Lobe (Top Gyri)
                g.DrawBezier(pBr, 7.5f*s, 2.2f*s, 5.8f*s, 2.0f*s, 5.2f*s, 4.2f*s, 6.8f*s, 4.5f*s);
                g.DrawBezier(pHi, 7.5f*s, 2.0f*s, 5.8f*s, 1.8f*s, 5.2f*s, 4.0f*s, 6.8f*s, 4.3f*s);

                // Middle Lateral Lobe (Sulcus convolution)
                g.DrawBezier(pBr, 6.2f*s, 5.2f*s, 3.8f*s, 5.5f*s, 3.5f*s, 8.2f*s, 5.5f*s, 8.0f*s);
                g.DrawBezier(pHi, 6.2f*s, 5.0f*s, 3.8f*s, 5.3f*s, 3.5f*s, 8.0f*s, 5.5f*s, 7.8f*s);

                // Inferior Lobe (Temporal Gyri / Foot)
                g.DrawBezier(pBr, 5.0f*s, 8.8f*s, 2.2f*s, 9.5f*s, 1.8f*s, 14.0f*s, 4.2f*s, 14.2f*s);
                g.DrawBezier(pHi, 5.0f*s, 8.6f*s, 2.2f*s, 9.3f*s, 1.8f*s, 13.8f*s, 4.2f*s, 14.0f*s);

                // Neural Crossbar Bridge (connecting brain to center)
                g.DrawLine(pBr, 5.8f*s, 11.0f*s, 8.0f*s, 11.0f*s);
                g.DrawLine(pHi, 5.8f*s, 10.7f*s, 8.0f*s, 10.7f*s);
            }

            // 3. RIGHT HALF: SILICON HARDWARE (OPTICALLY TUNED NEON RED HIGHWAYS & NODES)
            Color neonRed = isDark ? Color.FromArgb(255, 255, 10, 50) : Color.FromArgb(255, 225, 25, 45);
            Color neonHotRed = isDark ? Color.FromArgb(255, 255, 80, 110) : Color.FromArgb(255, 240, 60, 80);
            Color whiteCore = Color.FromArgb(255, 255, 255, 255);

            float traceW = Math.Max(1.2f, 1.5f * s);
            using (Pen pTrace = new Pen(neonRed, traceW) { StartCap = LineCap.Round, EndCap = LineCap.Round, LineJoin = LineJoin.Round })
            {
                // Main Vertical/Diagonal Silicon Highway 1
                PointF[] tr1 = new PointF[] {
                    new PointF(8.5f * s, 2.5f * s),
                    new PointF(10.2f * s, 4.2f * s),
                    new PointF(10.2f * s, 6.8f * s),
                    new PointF(11.8f * s, 9.0f * s),
                    new PointF(11.8f * s, 11.5f * s),
                    new PointF(13.2f * s, 14.0f * s)
                };
                g.DrawLines(pTrace, tr1);

                // Secondary Diagonal Trace 2
                PointF[] tr2 = new PointF[] {
                    new PointF(9.5f * s, 4.5f * s),
                    new PointF(11.5f * s, 4.5f * s),
                    new PointF(13.5f * s, 7.8f * s),
                    new PointF(14.0f * s, 12.0f * s)
                };
                g.DrawLines(pTrace, tr2);

                // Silicon Crossbar Bus (connecting center to right leg)
                g.DrawLine(pTrace, 8.0f * s, 11.0f * s, 11.8f * s, 11.0f * s);
            }

            // Microchip Package (Rectangular chip with pins)
            float chipX = 9.2f * s;
            float chipY = 6.2f * s;
            float chipW = Math.Max(2.5f, 2.8f * s);
            float chipH = Math.Max(2.0f, 2.4f * s);
            using (Brush bChip = new SolidBrush(Color.FromArgb(255, 18, 2, 6)))
            using (Pen pChip = new Pen(neonRed, Math.Max(0.8f, 1.0f * s)))
            {
                g.FillRectangle(bChip, chipX, chipY, chipW, chipH);
                g.DrawRectangle(pChip, chipX, chipY, chipW, chipH);
            }

            // Glowing Solder Nodes (Vias) - Pure White Laser Core + Neon Red Halo
            float nodeR = Math.Max(1.4f, 1.6f * s);
            float coreR = Math.Max(0.6f, 0.8f * s);
            using (Brush bRing = new SolidBrush(neonRed))
            using (Brush bCore = new SolidBrush(whiteCore))
            {
                PointF[] nodePts = new PointF[] {
                    new PointF(8.5f * s, 2.5f * s),
                    new PointF(11.5f * s, 4.5f * s),
                    new PointF(11.8f * s, 11.0f * s),
                    new PointF(13.2f * s, 14.0f * s)
                };
                foreach (PointF pt in nodePts)
                {
                    g.FillEllipse(bRing, pt.X - nodeR, pt.Y - nodeR, nodeR * 2, nodeR * 2);
                    g.FillEllipse(bCore, pt.X - coreR, pt.Y - coreR, coreR * 2, coreR * 2);
                }
            }

            // Cut out the inner central eye triangle
            using (GraphicsPath pEye = new GraphicsPath())
            {
                pEye.AddPolygon(eyeTriangle);
                g.SetClip(pEye);
                g.Clear(Color.Transparent);
                g.ResetClip();
            }

            // 4. ULTRA-THIN 1px CRISP DUAL-COLOR HAIRLINE OUTER RIM
            Color rimL = isDark ? Color.FromArgb(245, 255, 255, 255) : Color.FromArgb(240, 30, 41, 59);
            Color rimR = isDark ? Color.FromArgb(245, 255, 20, 60) : Color.FromArgb(240, 220, 38, 38);
            float rimW = Math.Max(1.0f, 1.2f * s);

            using (Pen pRimL = new Pen(rimL, rimW) { StartCap = LineCap.Round, EndCap = LineCap.Round, LineJoin = LineJoin.Round })
            using (Pen pRimR = new Pen(rimR, rimW) { StartCap = LineCap.Round, EndCap = LineCap.Round, LineJoin = LineJoin.Round })
            {
                PointF[] rimPtsL = new PointF[] {
                    new PointF(8f * s, 0.5f * s),
                    new PointF(0.5f * s, 15.5f * s),
                    new PointF(4.8f * s, 15.5f * s),
                    new PointF(6.2f * s, 12.5f * s)
                };
                g.DrawLines(pRimL, rimPtsL);

                PointF[] rimPtsR = new PointF[] {
                    new PointF(8f * s, 0.5f * s),
                    new PointF(15.5f * s, 15.5f * s),
                    new PointF(11.2f * s, 15.5f * s),
                    new PointF(9.8f * s, 12.5f * s)
                };
                g.DrawLines(pRimR, rimPtsR);

                // Thin eye triangle rim
                using (Pen pEyeRim = new Pen(isDark ? Color.FromArgb(200, 220, 230, 245) : Color.FromArgb(200, 30, 41, 59), Math.Max(0.8f, 1.0f * s)))
                {
                    g.DrawPolygon(pEyeRim, eyeTriangle);
                }
            }
        }
        return bmp;
    }

    static string GenerateVectorSvg(bool isDark)
    {
        string frameL = isDark ? "#FFFFFF" : "#1E293B";
        string frameR = isDark ? "#FF0A3C" : "#DC2626";
        string brainColor = isDark ? "#E6EEF8" : "#3C4B5F";
        string brainHi = isDark ? "#FFFFFF" : "#8CA0B9";
        string neonRed = isDark ? "#FF0A32" : "#E1192D";
        string eyeRim = isDark ? "#CBD5E1" : "#1E293B";

        return string.Format(@"<svg xmlns=""http://www.w3.org/2000/svg"" viewBox=""0 0 16 16"" width=""16"" height=""16"">
  <!-- Hard Black Substrate Base for Maximum Structural Contrast -->
  <polygon points=""8,0.5 15.5,15.5 11.2,15.5 9.8,12.5 6.2,12.5 4.8,15.5 0.5,15.5"" fill=""#040408"" />

  <!-- Left: Human Brain Luminous 3D Lobes -->
  <path d=""M 7.5 2.2 C 5.8 2.0, 5.2 4.2, 6.8 4.5"" fill=""none"" stroke=""{0}"" stroke-width=""1.8"" stroke-linecap=""round"" />
  <path d=""M 7.5 2.0 C 5.8 1.8, 5.2 4.0, 6.8 4.3"" fill=""none"" stroke=""{1}"" stroke-width=""0.9"" stroke-linecap=""round"" />

  <path d=""M 6.2 5.2 C 3.8 5.5, 3.5 8.2, 5.5 8.0"" fill=""none"" stroke=""{0}"" stroke-width=""1.8"" stroke-linecap=""round"" />
  <path d=""M 6.2 5.0 C 3.8 5.3, 3.5 8.0, 5.5 7.8"" fill=""none"" stroke=""{1}"" stroke-width=""0.9"" stroke-linecap=""round"" />

  <path d=""M 5.0 8.8 C 2.2 9.5, 1.8 14.0, 4.2 14.2"" fill=""none"" stroke=""{0}"" stroke-width=""1.8"" stroke-linecap=""round"" />
  <path d=""M 5.0 8.6 C 2.2 9.3, 1.8 13.8, 4.2 14.0"" fill=""none"" stroke=""{1}"" stroke-width=""0.9"" stroke-linecap=""round"" />

  <line x1=""5.8"" y1=""11.0"" x2=""8.0"" y2=""11.0"" stroke=""{0}"" stroke-width=""1.8"" stroke-linecap=""round"" />
  <line x1=""5.8"" y1=""10.7"" x2=""8.0"" y2=""10.7"" stroke=""{1}"" stroke-width=""0.9"" stroke-linecap=""round"" />

  <!-- Right: Silicon Hardware Glowing Neon Red Highways -->
  <polyline points=""8.5,2.5 10.2,4.2 10.2,6.8 11.8,9.0 11.8,11.5 13.2,14.0"" fill=""none"" stroke=""{2}"" stroke-width=""1.4"" stroke-linecap=""round"" stroke-linejoin=""round"" />
  <polyline points=""9.5,4.5 11.5,4.5 13.5,7.8 14.0,12.0"" fill=""none"" stroke=""{2}"" stroke-width=""1.2"" stroke-linecap=""round"" stroke-linejoin=""round"" />
  <line x1=""8.0"" y1=""11.0"" x2=""11.8"" y2=""11.0"" stroke=""{2}"" stroke-width=""1.4"" stroke-linecap=""round"" />

  <!-- Microchip Package -->
  <rect x=""9.2"" y=""6.2"" width=""2.8"" height=""2.4"" fill=""#120206"" stroke=""{2}"" stroke-width=""0.9"" />

  <!-- Glowing Laser Solder Nodes -->
  <circle cx=""8.5"" cy=""2.5"" r=""1.5"" fill=""{2}"" />
  <circle cx=""8.5"" cy=""2.5"" r=""0.7"" fill=""#FFFFFF"" />
  <circle cx=""11.5"" cy=""4.5"" r=""1.5"" fill=""{2}"" />
  <circle cx=""11.5"" cy=""4.5"" r=""0.7"" fill=""#FFFFFF"" />
  <circle cx=""11.8"" cy=""11.0"" r=""1.5"" fill=""{2}"" />
  <circle cx=""11.8"" cy=""11.0"" r=""0.7"" fill=""#FFFFFF"" />
  <circle cx=""13.2"" cy=""14.0"" r=""1.5"" fill=""{2}"" />
  <circle cx=""13.2"" cy=""14.0"" r=""0.7"" fill=""#FFFFFF"" />

  <!-- Inner Triangular Cutout -->
  <polygon points=""8,5.2 6.4,9.8 9.6,9.8"" fill=""#040408"" stroke=""{3}"" stroke-width=""0.9"" />

  <!-- Thin Dual-Color Hairline Outer Rim -->
  <polyline points=""8,0.5 0.5,15.5 4.8,15.5 6.2,12.5"" fill=""none"" stroke=""{4}"" stroke-width=""1.1"" stroke-linecap=""round"" stroke-linejoin=""round"" />
  <polyline points=""8,0.5 15.5,15.5 11.2,15.5 9.8,12.5"" fill=""none"" stroke=""{5}"" stroke-width=""1.1"" stroke-linecap=""round"" stroke-linejoin=""round"" />
</svg>", brainColor, brainHi, neonRed, eyeRim, frameL, frameR);
    }
}
