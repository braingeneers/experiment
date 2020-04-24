from PIL import Image
import os 

UUID = os.environ['UUID']

images_to_analyze=[]
root='/public/groups/braingeneers/imaging/'+UUID+'/original/'
for path, subdirs, files in os.walk(root):
    for name in files:
        images_to_analyze.append(os.path.join(path, name))
        
# Function to change the image size
def changeImageSize(maxWidth, 
                    maxHeight, 
                    image):
    
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]

    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])

    newImage    = image.resize((newWidth, newHeight))
    return newImage
    
# Take two images for blending them together   
for image_to_analyze in images_to_analyze:
    image1 = Image.open(image_to_analyze)
    image2 = Image.open("./blend-this.jpg")

    # Make the images of uniform size
    image3 = changeImageSize(800, 500, image1)
    image4 = changeImageSize(800, 500, image2)

    # Make sure images got an alpha channel
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")

    alphaBlended2 = Image.blend(image5, image6, alpha=.08)
    #print(image_to_analyze)
    past_original=image_to_analyze.split('original')[1]
    before_original=image_to_analyze.split('original')[0]
    try:
        cut_off_jpg = image_to_analyze.rsplit('/', 1)[0]
        make_dir=before_original+'blend_analysis'+past_original
        os.makedirs(make_dir.rsplit('/', 1)[0])
    except:
        pass
    
    print('/public/groups/braingeneers/imaging/'+UUID+ \
                                     '/blend_analysis'+past_original+'.png')
    
    alphaBlended2= alphaBlended2.save('/public/groups/braingeneers/imaging/'+UUID+ \
                                     '/blend_analysis'+past_original+'.png') 

