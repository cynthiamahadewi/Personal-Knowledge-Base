# Transformer Architecture

## Summary

The **Transformer** is a deep learning architecture introduced in 2017 by Vaswani et al. that revolutionized sequence modeling by replacing recurrence with self-attention mechanisms. Unlike RNNs and LSTMs, Transformers process all tokens in a sequence simultaneously, enabling efficient parallel computation. Originally designed for machine translation, the architecture has become the foundation for modern AI systems across NLP, computer vision, and multimodal domains.

## Overview

The Transformer architecture was introduced in the landmark paper "Attention Is All You Need" (2017) by researchers at Google Brain. It represented a paradigm shift away from recurrent neural networks (**RNNs**) and **Long Short-Term Memory (LSTM)** networks, which process sequences sequentially. Instead, Transformers leverage **self-attention** to capture relationships between all tokens in parallel, dramatically improving training efficiency and scalability.

## Core Components

### Self-Attention

**Self-attention** is the fundamental mechanism that allows each token in a sequence to attend to all other tokens. For each token, the mechanism computes weighted sums based on three learned projections: **queries (Q)**, **keys (K)**, and **values (V)**. The attention weights determine how much each token should focus on every other token when building its representation.

### Multi-Head Attention

**Multi-head attention** extends self-attention by running multiple attention mechanisms in parallel. Each "head" learns to capture different types of relationships or patterns in the data—some may focus on syntactic structure, others on semantic meaning. The outputs from all heads are concatenated and linearly transformed to produce the final attention output.

### Positional Encoding

Since Transformers process all tokens simultaneously without inherent sequential ordering, **positional encodings** inject position information into the input embeddings. The original paper used sinusoidal functions of different frequencies, though learned positional embeddings are also common in modern variants.

### Feed-Forward Layers

After each attention sub-layer, the architecture applies **position-wise feed-forward networks**—fully connected layers applied independently to each position. These layers provide nonlinear transformations that enhance the model's representational capacity.

### Layer Normalization and Residual Connections

**Layer normalization** and **residual connections** (skip connections) are applied throughout the architecture to stabilize training and enable the construction of very deep networks. These techniques help mitigate vanishing gradients and improve convergence.

## Architecture Variants

### Encoder-Decoder Structure

The original Transformer used an **encoder-decoder** architecture for sequence-to-sequence tasks like machine translation. The encoder processes the input sequence, while the decoder generates the output sequence autoregressively, attending to both its own previous outputs and the encoder's representations.

### Encoder-Only Models

**BERT** (Bidirectional Encoder Representations from Transformers, 2018) popularized encoder-only architectures for tasks requiring understanding of input text, such as classification, named entity recognition, and question answering. These models process input bidirectionally and are typically fine-tuned for downstream tasks.

### Decoder-Only Models

**GPT** (Generative Pre-trained Transformer) and its successors (GPT-2, GPT-3, GPT-4) use decoder-only architectures optimized for autoregressive generation. These models predict the next token given all previous tokens and have proven highly effective for text generation and few-shot learning.

## Impact and Applications

The Transformer architecture has become the dominant paradigm in **natural language processing (NLP)**, powering state-of-the-art models for translation, summarization, question answering, and text generation. Its influence has expanded far beyond language:

- **Computer Vision**: The Vision Transformer (**ViT**) applies the architecture directly to image patches, achieving competitive or superior performance to convolutional neural networks
- **Audio Processing**: Models like Whisper use Transformers for speech recognition and audio generation
- **Reinforcement Learning**: Decision Transformers frame RL as sequence modeling
- **Multimodal Systems**: Models like CLIP and GPT-4 combine Transformers across vision and language

The architecture's scalability has enabled the training of increasingly large models, leading to emergent capabilities and the current era of large language models.

## Related Concepts

- [[Attention Mechanism]]
- [[BERT]]
- [[GPT Architecture]]
- [[Vision Transformer]]
- [[Large Language Models]]
- [[Positional Encoding]]

## Tags

#transformer #attention-mechanism #deep-learning #neural-networks #nlp