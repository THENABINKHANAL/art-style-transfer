
import torch
import torch.nn as nn
import torch.nn.functional as F
import base64
from io import BytesIO
from torchvision import transforms
from PIL import Image
import io

class ResidualBlock(nn.Module):
    def __init__(self, in_features):
        super(ResidualBlock, self).__init__()
        
        self.block = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(in_features, in_features, 3),
            nn.InstanceNorm2d(in_features),
            nn.ReLU(True),
            nn.ReflectionPad2d(1),
            nn.Conv2d(in_features, in_features, 3),
            nn.InstanceNorm2d(in_features)
        )

    def forward(self, x):
        return x + self.block(x)

class Generator(nn.Module):
    def __init__(self, input_nc, output_nc, n_residual_blocks=9):
        super(Generator, self).__init__()

        # Initial convolution block       
        model = [
            nn.ReflectionPad2d(3),
            nn.Conv2d(input_nc, 64, 7),
            nn.InstanceNorm2d(64),
            nn.ReLU(True)
        ]

        # Downsampling
        in_features = 64
        out_features = in_features*2
        for _ in range(2):
            model += [
                nn.Conv2d(in_features, out_features, 3, stride=2, padding=1),
                nn.InstanceNorm2d(out_features),
                nn.ReLU(True)
            ]
            in_features = out_features
            out_features = in_features*2

        # Residual blocks
        for _ in range(n_residual_blocks):
            model += [ResidualBlock(in_features)]

        # Upsampling
        out_features = in_features//2
        for _ in range(2):
            model += [
                nn.ConvTranspose2d(in_features, out_features, 3, stride=2, padding=1, output_padding=1),
                nn.InstanceNorm2d(out_features),
                nn.ReLU(True)
            ]
            in_features = out_features
            out_features = in_features//2

        # Output layer
        model += [
            nn.ReflectionPad2d(3),
            nn.Conv2d(64, output_nc, 7),
            nn.Tanh()
        ]
        self.model = nn.Sequential(*model)

    def forward(self, x):
        return self.model(x)
    

class Discriminator(nn.Module):
    def __init__(self, input_nc):
        super(Discriminator, self).__init__()

        model = [
            nn.Conv2d(input_nc, 64, 4, stride=2, padding=1),
            nn.LeakyReLU(0.2, True)
        ]

        model += [
            nn.Conv2d(64, 128, 4, stride=2, padding=1),
            nn.InstanceNorm2d(128), 
            nn.LeakyReLU(0.2, True)
        ]

        model += [
            nn.Conv2d(128, 256, 4, stride=2, padding=1),
            nn.InstanceNorm2d(256), 
            nn.LeakyReLU(0.2, True)
        ]

        model += [
            nn.Conv2d(256, 512, 4, padding=1),
            nn.InstanceNorm2d(512), 
            nn.LeakyReLU(0.2, True)
        ]

        model += [nn.Conv2d(512, 1, 4, padding=1)]

        self.model = nn.Sequential(*model)

    def forward(self, x):
        return self.model(x)

def getResult(img_str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #device="cpu"
    # Models
    G_Y2X = Generator(3, 3).to(device)
    checkpointpaths = ['./Cubism_Final.pth', './Pointillism_Final.pth', './Realism_Final.pth']

    outputImages = []
    if img_str.startswith('data:image'):
        # Find the start of the base64 string
        img_str_offset = img_str.find('base64,') + len('base64,')
        # Grab the actual base64 content (after the comma)
        img_str = img_str[img_str_offset:]

    img_bytes = base64.b64decode(img_str)

    img_buf = io.BytesIO(img_bytes)

    # Byte stream to PIL Image
    image = Image.open(img_buf).convert('RGB')

    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])

    image_tensor = transform(image).unsqueeze(0).to(device)

    for checkpointpath in checkpointpaths:
        checkpoint = torch.load(checkpointpath, map_location=device)
        G_Y2X.load_state_dict(checkpoint['G_Y2X'])
        G_Y2X.eval()

        with torch.no_grad():
            fake_image_tensor = G_Y2X(image_tensor)
        
        fake_image = transforms.ToPILImage()(fake_image_tensor.squeeze().cpu() * 0.5 + 0.5)
        fake_image = fake_image.resize((512, 512))

        buffered = BytesIO()
        fake_image.save(buffered, format="JPEG")

        img_str = base64.b64encode(buffered.getvalue()).decode()
        outputImages.append({
            "dataSource": f"data:image/jpeg;base64,{img_str}"
        })
    return outputImages