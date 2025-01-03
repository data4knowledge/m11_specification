# Prompt

The code did not run succesfully. I think this is due to the colors used for the red and blue, they are shades of red and blue. Use the shades of the colors seen in the PDF documents to fix the code

# Prompt Response

I've updated the _extract_color_from_text method to be more flexible in detecting colors. Instead of looking for exact RGB values, it now:

Detects red when:
Red component > 0.7 (high red)
Green component < 0.3 (low green)
Blue component < 0.3 (low blue)
Detects blue when:
Red component < 0.3 (low red)
Green component < 0.3 (low green)
Blue component > 0.7 (high blue)
This should better handle the various shades of red and blue that appear in the PDF documents. The thresholds (0.7 and 0.3) are chosen to accommodate different shades while still maintaining clear distinction between colors.

Would you like to test this updated version with your PDF files to confirm it correctly identifies the colors?