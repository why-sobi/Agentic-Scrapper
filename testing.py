from bs4 import BeautifulSoup


html = """<article class='lzd-article'>
<ul><li><div><span>Xbox one
</span></div></li><li><div><span>With 1 Wireless Controller
</span></div></li><li><div><span>Xbox one brand new condition
</span></div></li><li><div><span>Xbox one complete accessories
</span></div></li><li><div><span>Never used in Pakistan
</span></div></li><li><div><span>Data Storage Capacity. 500GB Hard Drive Capacity</span></div></li><li><div><span>Output Type: HDMI</span></div></li><li><div><span>Color. Black
</span></div></li><li><div><span>1 x Console</span></div></li><li><div><span>1 x Controller</span></div></li><li><div><span>1 x Power supply</span></div></li></ul>
</article>"""

html2 = """<article style="white-space:break-spaces" class="lzd-article"><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span>Product Details of Gaming console Xbox one x</span></p><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span>● 1TB Hard Drive</span></p><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span>● 1x wireless Controller</span></p><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span>● 1x Hdmi Cable {Orignal}</span></p><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span>● 1x Power Cable {Orignal}</span></p><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span>● 1x Power Supply</span></p><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span>● Secure Packing -✔</span></p><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span>note: Offline bundle is free for first time</span></p><p style="line-height:1.7;text-align:left;text-indent:0;margin-left:0;margin-top:0;margin-bottom:0"><span></span><img style="width:2000px;height:2000px;display:inline;vertical-align:middle" src="https://img.drz.lazcdn.com/static/pk/p/1b8c3d46ae27dea984568ee1c95ff2ee.jpg_2200x2200q80.jpg_.webp"><span> </span></p></article>"""

parser = BeautifulSoup(html2, features='html.parser')
print(parser.get_text(separator='\n'))