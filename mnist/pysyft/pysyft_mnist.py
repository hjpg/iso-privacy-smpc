from mnist.common.constants import CONVNET_MODEL_PATH, TEST_BATCH_SIZE, CONV_MODEL_TYPE
from mnist.common.mnist_training import train_mnist_model
from common.pysyft.pysyft_private_inference import PysyftPrivateInference
from mnist.pysyft.private_mnist_data_loader import PrivateMnistDataLoader

should_train = False
if should_train:
    train_mnist_model(CONV_MODEL_TYPE, 'mnist/models/alice_conv_model.pth')

smpc_mnist = PysyftPrivateInference(PrivateMnistDataLoader(), parameters={'test_batch_size': TEST_BATCH_SIZE})
smpc_mnist.perform_inference('mnist/models/alice_conv_model.pth')
