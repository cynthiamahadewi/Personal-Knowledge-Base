# Convolutional Neural Networks

## Summary

**Convolutional Neural Networks (CNNs)** are a class of deep learning models specifically designed for processing grid-structured data such as images. They leverage **local connectivity** and **weight sharing** through convolutional filters to automatically learn spatial hierarchies of features, making them highly effective for visual recognition tasks.

## Core Components

### Convolutional Layer

The **convolutional layer** is the fundamental building block of CNNs. It applies learned filters (also called kernels) across the spatial dimensions of the input data. Each filter slides across the input, computing dot products to produce **feature maps** that capture local patterns such as edges, textures, or more complex structures in deeper layers.

### Activation Function

After convolution, an **activation function** introduces non-linearity into the network. The most commonly used activation is **ReLU (Rectified Linear Unit)**, defined as f(x) = max(0, x). ReLU helps networks learn complex patterns while being computationally efficient and reducing the vanishing gradient problem.

### Pooling Layer

**Pooling layers** reduce the spatial dimensions of feature maps through operations like **max pooling** or **average pooling**. This downsampling serves two purposes: it reduces computational cost and provides a degree of **translational invariance**, making the network more robust to small shifts in input position.

### Fully Connected Layer

The final layers of a CNN typically consist of **fully connected layers** that aggregate the learned spatial features and map them to output classes for classification tasks or continuous values for regression tasks.

## Architectural Innovations

### AlexNet (2012)

**AlexNet** was the first deep CNN to win the ImageNet competition, marking a breakthrough moment for deep learning. It introduced the widespread use of ReLU activations and **dropout** for regularization, demonstrating that deep networks could be effectively trained on large-scale image datasets.

### VGG (2014)

The **VGG architecture** explored the use of very deep networks built entirely from small 3×3 convolutional filters. This design showed that network depth is a critical component for good performance, and the uniform architecture made it easy to understand and implement.

### ResNet (2015)

**ResNet (Residual Networks)** introduced **skip connections** (or residual connections) that allow gradient flow directly through the network. This innovation enabled the training of extremely deep networks with 100+ layers by addressing the degradation problem that plagued very deep architectures.

### EfficientNet (2019)

**EfficientNet** introduced a principled approach to scaling CNNs through **compound scaling** that simultaneously adjusts network depth, width, and input resolution. This method achieves better accuracy and efficiency compared to scaling only one dimension.

## Applications

CNNs have become the foundation for numerous computer vision applications:

- **Image classification**: Categorizing entire images into predefined classes
- **Object detection**: Locating and classifying multiple objects within images using architectures like **YOLO** and **Faster R-CNN**
- **Semantic segmentation**: Pixel-level classification of image regions
- **Face recognition**: Identity verification and facial analysis
- **Medical imaging**: Disease detection and diagnosis from X-rays, MRIs, and CT scans

## Limitations and Modern Alternatives

Despite their success, CNNs have inherent limitations. They possess a **limited global receptive field** unless networks are made very deep, meaning they may struggle to capture long-range dependencies in images. **Vision Transformers (ViT)** have emerged as a powerful alternative by applying **self-attention mechanisms** directly to image patches, challenging CNN dominance in many computer vision tasks by better capturing global context.

## Related Concepts

- [[Deep Learning]]
- [[Vision Transformers]]
- [[Backpropagation]]
- [[Transfer Learning]]
- [[Object Detection]]
- [[Image Segmentation]]

## Tags

#convolutional-neural-networks #computer-vision #deep-learning #image-classification #neural-networks