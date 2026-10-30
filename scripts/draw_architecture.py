from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math
S=2; W,H=1600,1050
im=Image.new('RGB',(W*S,H*S),'#f5f7fa');d=ImageDraw.Draw(im)
navy='#232f3e';gray='#536477';orange='#ff9900';purple='#8c4fff';green='#3f8624';blue='#147eba'
def font(n,b=False):return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial'+(' Bold' if b else '')+'.ttf',n*S)
def text(x,y,t,n=20,c=navy,b=False):d.text((x*S,y*S),t,font=font(n,b),fill=c)
def box(x,y,w,h,fill='white',outline='#dae1e9',r=14,width=2):d.rounded_rectangle((x*S,y*S,(x+w)*S,(y+h)*S),r*S,fill=fill,outline=outline,width=width*S)
def line(points,c=gray,width=3):d.line([(x*S,y*S) for x,y in points],fill=c,width=width*S)
def arrow(points,c=gray,dashed=False):
 if dashed:
  for a,b in zip(points,points[1:]):
   length=math.dist(a,b)
   for i in range(0,int(length),16):
    j=min(i+9,length);line([(a[0]+(b[0]-a[0])*i/length,a[1]+(b[1]-a[1])*i/length),(a[0]+(b[0]-a[0])*j/length,a[1]+(b[1]-a[1])*j/length)],c,2)
 else:line(points,c)
 a,b=points[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);p=[b,(b[0]-12*math.cos(ang-.45),b[1]-12*math.sin(ang-.45)),(b[0]-12*math.cos(ang+.45),b[1]-12*math.sin(ang+.45))];d.polygon([(x*S,y*S) for x,y in p],fill=c)
def icon(x,y,color,kind):
 box(x,y,64,64,color,color,9)
 if kind=='bucket':
  line([(x+17,y+21),(x+22,y+49),(x+43,y+49),(x+48,y+21)],'white',3)
  d.ellipse(((x+17)*S,(y+14)*S,(x+48)*S,(y+27)*S),outline='white',width=3*S)
 elif kind=='cdn':
  d.ellipse(((x+13)*S,(y+13)*S,(x+51)*S,(y+51)*S),outline='white',width=2*S)
  d.ellipse(((x+24)*S,(y+13)*S,(x+40)*S,(y+51)*S),outline='white',width=2*S)
  line([(x+13,y+32),(x+51,y+32)],'white',2)
 elif kind=='lock':
  box(x+19,y+28,27,23,color,'white',3,2)
  d.arc(((x+23)*S,(y+12)*S,(x+42)*S,(y+38)*S),180,360,fill='white',width=3*S)
 elif kind=='user':
  d.ellipse(((x+25)*S,(y+12)*S,(x+40)*S,(y+27)*S),outline='white',width=3*S)
  d.arc(((x+16)*S,(y+32)*S,(x+49)*S,(y+61)*S),180,360,fill='white',width=3*S)
 else:text(x+15,y+16,kind,25,'white',True)
def card(x,y,w,h,title,sub,color,kind):
 box(x,y,w,h);icon(x+20,y+20,color,kind);text(x+20,y+103,title,22,b=True)
 for i,t in enumerate(sub):text(x+20,y+140+i*25,t,17,gray)
# cloud boundary
box(340,184,1210,360,'#ffffff','#ff9900',16)
text(364,201,'AWS CLOUD',17,'#b56700',True)
text(1270,202,'Public HTTPS endpoint',16,gray)
card(48,265,235,245,'Visitors',[],blue,'user')
card(385,265,290,245,'Amazon CloudFront',['HTTPS + edge caching','Generated CloudFront URL'],purple,'cdn')
card(771,265,290,245,'Origin Access Control',['Signed origin requests','CloudFront-only reads'], '#c76b16','lock')
card(1157,265,340,245,'Amazon S3',['Private website bucket','HTML · CSS · JavaScript','Portrait · Logos · Resume PDF'],green,'bucket')
arrow([(283,375),(385,375)]);text(296,341,'HTTPS',15,gray,True)
arrow([(675,375),(771,375)]);text(690,341,'Fetch',15,gray)
arrow([(1061,375),(1157,375)]);text(1071,341,'Signed',15,gray)
# lower band
text(48,588,'INFRASTRUCTURE & RELEASE FLOW',18,navy,True)
card(48,640,320,205,'GitHub repository',['EpicCoder71/cloud-resume','Website + Terraform source'],navy,'Git')
card(430,640,320,205,'Terraform · local',['Provisions S3, CloudFront, IAM','Local state excluded from Git'],'#7144c1','IaC')
card(820,640,320,205,'AWS CLI · local',['Syncs website files to S3','Invalidates CloudFront cache'],blue,'>_')
box(1200,640,350,205,'#fff9ee','#eccb90')
text(1222,661,'CI/CD FOUNDATION',17,'#995700',True)
text(1222,702,'GitHub OIDC + IAM role',20,navy,True)
text(1222,738,'Provisioned with Terraform',17,gray)
text(1222,766,'Automatic GitHub Actions',17,gray)
text(1222,791,'deployment: not yet enabled',17,gray)
arrow([(368,740),(430,740)]);text(375,710,'IaC',14,gray)
arrow([(590,640),(590,578),(530,578),(530,544)],'#7144c1',True)
text(602,555,'Provision & configure',16,'#7144c1')
arrow([(980,640),(980,578),(1327,578),(1327,544)],blue,True)
text(1084,551,'Upload site files',16,blue)
# Export only the architecture diagram, without a title banner or footer.
im=im.crop((20*S,165*S,1580*S,870*S))
root=Path(__file__).resolve().parents[1]
out=root/'site/assets/cloud-resume-architecture.png'
im.save(out)
print(out)
