"""
Trains a PyTorch image classification model using device-agnostic code.
"""

import os
import torch

import data_setup, engine, model_builder, utils
import argparse

from torchvision import transforms

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--MODEL")
    parser.add_argument("--TRAINED", default=False)
    parser.add_argument("--EPOCHS")
    parser.add_argument("--BATCH_SIZE", default=8)

    args = parser.parse_args()

    # Setup hyperparameters
    NUM_EPOCHS = int(args.EPOCHS)
    BATCH_SIZE = int(args.BATCH_SIZE)
    LEARNING_RATE = 0.001

    # Setup directories
    train_dir = "Datasets/train"
    test_dir = "Datasets/valid"

    # Setup target device
    device = "cuda" if torch.cuda.is_available() else "cpu" 

    # Create transforms
    data_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])


    # Create DataLoaders with help from data_setup.py
    train_dataloader, test_dataloader, class_names = data_setup.create_dataloaders(
        train_dir=train_dir,
        test_dir=test_dir,
        transform=data_transform,
        batch_size=BATCH_SIZE
    )

    # Create model with help from model_builder.py
    
    model_name = args.MODEL.strip().lower()
    torch.cuda.manual_seed(42)
    torch.manual_seed(42)

    if model_name == "vgg19":
        model = model_builder.VGG19(
            num_classes=len(class_names)
        )
        model_name = "VGG19"

    elif model_name == "resnet18":
        model = model_builder.ResNet18(
            num_classes=len(class_names)
        )
        model_name = "ResNet18"

    elif model_name == "mnasnet":
        model = model_builder.MnasNet(
            num_classes=len(class_names)
        )
        model_name = "MnasNet"
    
    elif model_name == "mobilenetv3":
        model = model_builder.MobileNetV3(
            num_classes=len(class_names)
        )
        model_name = "MobileNetV3"

    elif model_name == "alexnet":
        model = model_builder.AlexNet(
            num_classes=len(class_names)
        )
        model_name = "AlexNet"

    elif model_name == "shufflenetv2":
        model = model_builder.ShuffleNetV2(
            num_classes=len(class_names)
        )
        model_name = "ShuffleNetv2"

    
    elif model_name == "squeezenet":
        model = model_builder.ShuffleNetV2(
            num_classes=len(class_names)
        )
        model_name = "SqueezeNet"

    
    elif model_name == "efficientnet":
        model = model_builder.EfficientNet(
            num_classes=len(class_names)
        )
        model_name = "EfficientNet"

    else :
        raise Exception("Wrong Model.")
    


    trained = True if args.TRAINED == "True" else False if args.TRAINED == "False" else None
    if trained == None:
        raise Exception("Wrong Argument --TRAINED, \"True\" or \"False\".")

    # Load if pre-trained
    if trained:
        model_data = utils.load_model(file_dir = "models", model_name = f"{model_name}.pth")
        model = model_data["model"]
    
    # Set loss and optimizer
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(),
                                lr=LEARNING_RATE)

    # Load previous training data if available
    if trained:
        prev_res = utils.load_data(model_name)
    else:
        prev_res = None

    # Start training with help from engine.py
    model.to(device)
    results = engine.train(model=model,
                train_dataloader=train_dataloader,
                test_dataloader=test_dataloader,
                loss_fn=loss_fn,
                optimizer=optimizer,
                epochs=NUM_EPOCHS,
                device=device,
                results=prev_res)

    # Save the model with help from utils.py
    utils.save_model(model=model,
                    target_dir="models",
                    model_name=f"{model_name}.pth",
                    class_names=class_names)

    # Save the training data with the help from utils.py
    utils.save_data(
        model_name,
        results
    )
    
