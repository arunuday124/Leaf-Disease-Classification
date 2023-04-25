"""
Contains PyTorch model code to instantiate a VGG19 model.
"""
import torch
from torch import nn
import torch.nn.functional as F

### VGG19

class VGG19(nn.Module):
    """
    Creates the VGG19 architecture.

    Replicates the VGG19, the a convolutional neural network introduced by Karen Simonyan, that consists of 19 layers, 16 convolution layers, and three fully connected layers.
    Original Resource : https://arxiv.org/abs/1409.1556 

    Args:
    num_classes: An integer indicating number of output units.
    kernel_size: An integer indicating number N for N x N shaped kernel box.
    padding: An integer indicating number of hidden outer values for each layer.
    padding: An integer indicating number of steps skipped for each iteration for kernel.
    """
    def __init__(self, num_classes=10, kernel_size=3, padding=1, stride=1):
        super(VGG19, self).__init__()
        self.conv_1_1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )
        self.conv_1_2 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )
        self.conv_2_1 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(128),
            nn.ReLU()
        )
        self.conv_2_2 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(128),
            nn.ReLU()
        )
        self.conv_3_1 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(256),
            nn.ReLU()
        )
        self.conv_3_2 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(256),
            nn.ReLU()
        )
        self.conv_3_3 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(256),
            nn.ReLU()
        )
        self.conv_3_4 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(256),
            nn.ReLU()
        )
        self.conv_4_1 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.conv_4_2 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.conv_4_3 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.conv_4_4 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.conv_5_1 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.conv_5_2 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.conv_5_3 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.conv_5_4 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(7*7*512, 4096),
            nn.ReLU()
        )
        self.fc1 = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU()
        )
        self.fc2= nn.Sequential(
            nn.Linear(4096, num_classes)
        )

        self.pool = nn.MaxPool2d(kernel_size = 2, stride = 2)
        
    def forward(self, x):
        out = self.conv_1_1(x)
        out = self.conv_1_2(out)
        out = self.pool(out)
        out = self.conv_2_1(out)
        out = self.conv_2_2(out)
        out = self.pool(out)
        out = self.conv_3_1(out)
        out = self.conv_3_2(out)
        out = self.conv_3_3(out)
        out = self.conv_3_4(out)
        out = self.pool(out)
        out = self.conv_4_1(out)
        out = self.conv_4_2(out)
        out = self.conv_4_3(out)
        out = self.conv_4_4(out)
        out = self.pool(out)
        out = self.conv_5_1(out)
        out = self.conv_5_2(out)
        out = self.conv_5_3(out)
        out = self.conv_5_4(out)
        out = self.pool(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        out = self.fc1(out)
        out = self.fc2(out)
        return out



### ResNet18

class Block(nn.Module):

    """
     a basic ResNet18 building block. It differs a little from larger ResNet architectures, but the overall logic is the same. The block consist of two convolutional layers and supports skip connections.
    """
    
    def __init__(self, in_channels, out_channels, identity_downsample=None, stride=1):
        super(Block, self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()
        self.identity_downsample = identity_downsample
        
    def forward(self, x):

        identity = x
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        if self.identity_downsample is not None:
            identity = self.identity_downsample(identity)
        x += identity
        x = self.relu(x)

        return x

class ResNet18(nn.Module):
    """
    ResNet18 architecture. It has some feature extraction at the beginning and four ResNet blocks with skip connections. At the end we use adaptive average pooling (for the model to be agnostic to the input image size) and a fully-connected layer.

        Args:
            image_channels (int) : Number of image channels to be processed in the model.
            num_of_classes (int) : Number of classes in which the model will classify images into.
    """

    def __init__(self, num_classes: int):
        super(ResNet18, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        
        # resnet layers
        self.layer1 = self.__make_layer(64, 64, stride=1)
        self.layer2 = self.__make_layer(64, 128, stride=2)
        self.layer3 = self.__make_layer(128, 256, stride=2)
        self.layer4 = self.__make_layer(256, 512, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)


    def __make_layer(self, in_channels, out_channels, stride) -> nn.Sequential:
        
        identity_downsample = None
        if stride != 1:
            identity_downsample = self.identity_downsample(in_channels, out_channels)
            
        return nn.Sequential(
            Block(in_channels, out_channels, identity_downsample=identity_downsample, stride=stride), 
            Block(out_channels, out_channels)
        )


    def identity_downsample(self, in_channels, out_channels) -> nn.Sequential:
        
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1), 
            nn.BatchNorm2d(out_channels)
        )


    def forward(self, x):
        
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        
        x = self.avgpool(x)
        x = x.view(x.shape[0], -1)
        x = self.fc(x)
        return x 


### MobileNetV3

class Hswish(nn.Module):
    def forward(self, x):
        return x * F.relu6(x + 3, inplace=True) / 6

class Hsigmoid(nn.Module):
    def forward(self, x):
        return F.relu6(x + 3, inplace=True) / 6

class SqueezeExcitation(nn.Module):
    def __init__(self, in_channels, reduced_channels):
        super(SqueezeExcitation, self).__init__()
        self.se = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Conv2d(in_channels, reduced_channels, kernel_size=1, stride=1, padding=0),
            Hswish(),
            nn.Conv2d(reduced_channels, in_channels, kernel_size=1, stride=1, padding=0),
            Hsigmoid()
        )

    def forward(self, x):
        se = self.se(x)
        return x * se

class InvertedResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride, expansion_factor):
        super(InvertedResidualBlock, self).__init__()
        hidden_dim = int(round(in_channels * expansion_factor))

        self.use_residual = stride == 1 and in_channels == out_channels

        layers = []
        if expansion_factor != 1:
            layers.append(nn.Conv2d(in_channels, hidden_dim, kernel_size=1, stride=1, padding=0, bias=False))
            layers.append(nn.BatchNorm2d(hidden_dim))
            layers.append(Hswish())

        layers.append(nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, stride=stride, padding=1, groups=hidden_dim, bias=False))
        layers.append(nn.BatchNorm2d(hidden_dim))
        layers.append(Hswish())

        layers.append(nn.Conv2d(hidden_dim, out_channels, kernel_size=1, stride=1, padding=0, bias=False))
        layers.append(nn.BatchNorm2d(out_channels))

        self.block = nn.Sequential(*layers)

    def forward(self, x):
        if self.use_residual:
            return x + self.block(x)
        else:
            return self.block(x)

class MobileNetV3_Stem(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(MobileNetV3_Stem, self).__init__()
        self.stem = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            Hswish()
        )

    def forward(self, x):
        return self.stem(x)

class Bottlenecks(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, expansion_factor, repeat):
        super(Bottlenecks, self).__init__()
        layers = []
        for i in range(repeat):
            if i == 0:
                layers.append(InvertedResidualBlock(in_channels, out_channels, stride, expansion_factor))
            else:
                layers.append(InvertedResidualBlock(out_channels, out_channels, 1, expansion_factor))
        self.bottlenecks = nn.Sequential(*layers)

    def forward(self, x):
        return self.bottlenecks(x)

class Classifier(nn.Module):
    def __init__(self, in_channels, num_classes):
        super(Classifier, self).__init__()
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.conv1 = nn.Conv2d(in_channels, 1280, kernel_size=1, stride=1, padding=0, bias=True)
        self.hswish1 = Hswish()
        self.dropout = nn.Dropout(p=0.2, inplace=True)
        self.conv2 = nn.Conv2d(1280, num_classes, kernel_size=1, stride=1, padding=0, bias=True)

    def forward(self, x):
        x = self.avgpool(x)
        x = self.conv1(x)
        x = self.hswish1(x)
        x = self.dropout(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        return x

class MobileNetV3(nn.Module):
    def __init__(self, num_classes=1000):
        super(MobileNetV3, self).__init__()
        self.stem = MobileNetV3_Stem(3, 16)
        self.bottlenecks = nn.Sequential(
            InvertedResidualBlock(16, 16, 2, 1),
            InvertedResidualBlock(16, 24, 2, 2),
            InvertedResidualBlock(24, 40, 2, 2),
            InvertedResidualBlock(40, 80, 2, 1),
            InvertedResidualBlock(80, 160, 2, 2),
            InvertedResidualBlock(160, 320, 2, 1),
            InvertedResidualBlock(320, 640, 2, 1),
            InvertedResidualBlock(640, 1280, 2, 1),
        )
        self.classifier = Classifier(1280, num_classes)

    def forward(self, x):
        x = self.stem(x)
        x = self.bottlenecks(x)
        x = self.classifier(x)
        return x


### SqueezeNet

class Fire(nn.Module):
    def __init__(self, inplanes: int, squeeze_planes: int, expand1x1_planes: int, expand3x3_planes: int) -> None:
        super().__init__()
        self.inplanes = inplanes
        self.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_activation = nn.ReLU(inplace=True)
        self.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes, kernel_size=1)
        self.expand1x1_activation = nn.ReLU(inplace=True)
        self.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes, kernel_size=3, padding=1)
        self.expand3x3_activation = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.squeeze_activation(self.squeeze(x))
        return torch.cat(
            [self.expand1x1_activation(self.expand1x1(x)), self.expand3x3_activation(self.expand3x3(x))], 1
        )


class SqueezeNet(nn.Module):
    def __init__(self, version: str = "1_0", num_classes: int = 1000, dropout: float = 0.5) -> None:
        super().__init__()
        _log_api_usage_once(self)
        self.num_classes = num_classes
        if version == "1_0":
            self.features = nn.Sequential(
                nn.Conv2d(3, 96, kernel_size=7, stride=2),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
                Fire(96, 16, 64, 64),
                Fire(128, 16, 64, 64),
                Fire(128, 32, 128, 128),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
                Fire(256, 32, 128, 128),
                Fire(256, 48, 192, 192),
                Fire(384, 48, 192, 192),
                Fire(384, 64, 256, 256),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
                Fire(512, 64, 256, 256),
            )
        elif version == "1_1":
            self.features = nn.Sequential(
                nn.Conv2d(3, 64, kernel_size=3, stride=2),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
                Fire(64, 16, 64, 64),
                Fire(128, 16, 64, 64),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
                Fire(128, 32, 128, 128),
                Fire(256, 32, 128, 128),
                nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
                Fire(256, 48, 192, 192),
                Fire(384, 48, 192, 192),
                Fire(384, 64, 256, 256),
                Fire(512, 64, 256, 256),
            )
        else:
            # FIXME: Is this needed? SqueezeNet should only be called from the
            # FIXME: squeezenet1_x() functions
            # FIXME: This checking is not done for the other models
            raise ValueError(f"Unsupported SqueezeNet version {version}: 1_0 or 1_1 expected")

        # Final convolution is initialized differently from the rest
        final_conv = nn.Conv2d(512, self.num_classes, kernel_size=1)
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout), final_conv, nn.ReLU(inplace=True), nn.AdaptiveAvgPool2d((1, 1))
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if m is final_conv:
                    init.normal_(m.weight, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform_(m.weight)
                if m.bias is not None:
                    init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.classifier(x)
        return torch.flatten(x, 1)


### MnasNet

class InvertedResidual(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, expansion_factor):
        super().__init__()
        self.stride = stride
        self.use_residual = in_channels == out_channels and stride == 1
        hidden_dim = int(in_channels * expansion_factor)
        self.expand = nn.Sequential(
            nn.Conv2d(in_channels, hidden_dim, kernel_size=1, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True)
        )
        self.depthwise = nn.Sequential(
            nn.Conv2d(hidden_dim, hidden_dim, kernel_size=kernel_size,
                      stride=stride, padding=kernel_size // 2,
                      groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True)
        )
        self.project = nn.Sequential(
            nn.Conv2d(hidden_dim, out_channels, kernel_size=1,
                      bias=False),
            nn.BatchNorm2d(out_channels)
        )

    def forward(self, x):
        if self.use_residual:
            return x + self.project(self.depthwise(self.expand(x)))
        else:
            return self.project(self.depthwise(self.expand(x)))

class MnasNet(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
        self.num_classes = num_classes
        self.stem = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3,
                      stride=2, padding=1,
                      bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU6(inplace=True)
        )
        self.layers = nn.Sequential(
            InvertedResidual(32, 16, 3, 1, 1),
            InvertedResidual(16, 24, 3, 2, 6),
            InvertedResidual(24, 24, 3, 1, 6),
            InvertedResidual(24, 40, 5, 2, 6),
            InvertedResidual(40, 40, 5, 1, 6),
            InvertedResidual(40, 40, 5, 1, 6),
            InvertedResidual(40, 80, 3, 2, 6),
            InvertedResidual(80, 80, 3, 1 ,6),
            InvertedResidual(80 ,80 ,3 ,1 ,6),
            InvertedResidual(80 ,96 ,3 ,1 ,6),
            InvertedResidual(96 ,96 ,3 ,1 ,6),
            InvertedResidual(96 ,192 ,5 ,2 ,6),
            InvertedResidual(192 ,192 ,5 ,1 ,6),
            InvertedResidual(192 ,192 ,5 ,1 ,6),
            InvertedResidual(192 ,320 ,3 ,1 ,6)
        )
        self.head = nn.Sequential(
            nn.Conv2d(320 ,1280 ,kernel_size=1 ,
                      bias=False),
            nn.BatchNorm2d(1280),
            nn.ReLU6(inplace=True)
        )
        self.avgpool = nn.AdaptiveAvgPool2d((1))
        self.classifier = nn.Linear(1280,num_classes)

    def forward(self,x):
        x = self.stem(x)
        x = self.layers(x)
        x = self.head(x)
        x = self.avgpool(x)
        x = x.view(-1,x.shape[1])
        x = self.classifier(x)
        return x
