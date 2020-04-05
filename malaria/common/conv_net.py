from torch import nn
import torch.nn.functional as F


class ConvNet(nn.Module):
    """
    A custom CNN network.
    """

    def __init__(self, in_channels, num_classes, conv_kernel_sizes, channels, max_pool_sizes, fc_units):
        """
        Creates a CNN.
        :param in_channels: the number of input channels.
        :param num_classes: the number of classes.
        :param conv_kernel_sizes: an array containing the kernel sizes for each convolution.
        :param channels: an array containing the channels for each convolution.
        :param max_pool_sizes: an array containing the maxpool sizes for the maxpool layers.
        :param fc_units: an array containing the number of units in the fully connected layers.
        """
        super(ConvNet, self).__init__()

        self.conv_1 = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=channels[0], kernel_size=conv_kernel_sizes[0], stride=1),
        )
        self.batch_norm_1 = nn.BatchNorm2d(channels[0])

        self.max_pool_1 = nn.MaxPool2d(kernel_size=max_pool_sizes[0])

        self.conv_2 = nn.Sequential(
            nn.Conv2d(in_channels=channels[0], out_channels=channels[1], kernel_size=conv_kernel_sizes[1], stride=1),
        )
        self.batch_norm_2 = nn.BatchNorm2d(channels[1])

        self.max_pool_2 = nn.MaxPool2d(kernel_size=max_pool_sizes[1])

        self.fc_1 = nn.Sequential(
            nn.Flatten(),
            nn.Linear(channels[1]*5*5, fc_units[0]),
        )
        self.batch_norm_3 = nn.BatchNorm1d(fc_units[0])

        self.fc_2 = nn.Sequential(
            nn.Linear(fc_units[0], num_classes),
        )

    def forward(self, x):
        """
        Computes the forward pass of the network without applying the final activation as this is done when computing
        the loss for efficiency.
        :param x: The input data.
        :return: The output after the forward pass.
        """
        x = self.conv_1(x)
        x = self.batch_norm_1(x)
        # PySyft doesn't work with the ReLU being part of the sequential module
        x = F.relu(x)
        x = F.avg_pool2d(x, kernel_size=2)

        x = self.conv_2(x)
        x = self.batch_norm_2(x)
        x = F.relu(x)
        x = F.avg_pool2d(x, kernel_size=2)

        x = self.fc_1(x)
        x = self.batch_norm_3(x)
        x = F.relu(x)

        out = self.fc_2(x)

        return out
