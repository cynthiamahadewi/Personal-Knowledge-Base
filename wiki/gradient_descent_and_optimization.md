# Gradient Descent and Optimization

## Summary

**Gradient descent** is the fundamental optimization algorithm used to train neural networks by iteratively updating model parameters in the direction that reduces the loss function. Modern deep learning relies on variants like mini-batch SGD and adaptive optimizers such as Adam, which adjust learning rates dynamically to improve convergence speed and stability.

## Core Algorithm

**Gradient descent** optimizes a model by minimizing a **loss function** L(θ) with respect to parameters θ. The algorithm repeatedly applies the update rule:

θ ← θ - η · ∇_θ L

where η is the **learning rate** and ∇_θ L is the gradient of the loss with respect to parameters.

## Variants

### Batch Gradient Descent

Computes gradients using the entire dataset for each update. Provides accurate gradient estimates but is computationally expensive and slow for large datasets.

### Stochastic Gradient Descent (SGD)

Updates parameters using only one training sample at a time. Introduces noise into the optimization process but enables much faster iterations and can help escape shallow local minima.

### Mini-Batch SGD

The standard approach in practice, using batches of 32-512 samples per update. Balances computational efficiency with gradient estimate quality and leverages GPU parallelization effectively.

## Adaptive Optimizers

**Adaptive optimizers** automatically adjust learning rates for each parameter based on gradient history:

**AdaGrad** adapts the learning rate per parameter using accumulated squared gradients, giving smaller updates to frequently updated parameters.

**RMSProp** improves on AdaGrad by using an exponential moving average of squared gradients, preventing learning rates from decreasing too aggressively.

**Adam** (Adaptive Moment Estimation) is the most widely used optimizer in deep learning. It combines momentum (first moment) and RMSProp (second moment) to maintain both the running average of gradients and their squared values.

## Learning Rate Scheduling

Using a constant learning rate is rarely optimal. Common **learning rate schedules** include:

- **Cosine annealing**: Smoothly decreases learning rate following a cosine curve
- **Linear warmup + decay**: Gradually increases then decreases learning rate
- **OneCycleLR**: Cycles learning rate within specified bounds

## Optimization Challenges

Deep neural network optimization faces several challenges:

- **Saddle points**: Points where gradient is zero but not a minimum
- **Vanishing/exploding gradients**: Gradients become too small or large in deep networks
- **Local minima**: Suboptimal solutions that trap optimization
- **Ill-conditioning**: Large variations in curvature across dimensions

Mitigation techniques include **gradient clipping** (capping gradient magnitude), **batch normalization** (normalizing layer inputs), and careful weight initialization.

## Second-Order Methods

**Second-order optimization methods** like Newton's method and L-BFGS use curvature information (second derivatives) for potentially faster convergence. However, they are rarely used in deep learning due to prohibitive memory requirements and computational costs when dealing with millions of parameters.

## Related Concepts

- [[Backpropagation]]
- [[Loss Functions]]
- [[Learning Rate]]
- [[Momentum]]
- [[Batch Normalization]]
- [[Neural Network Training]]

## Tags

#optimization #gradient-descent #neural-networks #training #deep-learning