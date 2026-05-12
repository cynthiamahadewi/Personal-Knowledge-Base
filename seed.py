"""
seed.py — Seed the knowledge base with foundational AI/ML topics.
Run this once to populate the raw/ directory with starter content.
Usage: python seed.py
"""

import sys
from pathlib import Path

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent))
from ingest import save_source

SEED_ARTICLES = [
    {
        "title": "Transformer Architecture",
        "content": """
The Transformer is a deep learning architecture introduced in the 2017 paper "Attention Is All You Need" by Vaswani et al. at Google Brain. Unlike earlier sequence models that relied on recurrence (RNNs, LSTMs), Transformers use a mechanism called self-attention to process all tokens in a sequence simultaneously.

Core components:
- Self-Attention: Each token attends to all other tokens, computing weighted sums based on query-key-value projections.
- Multi-Head Attention: Multiple attention heads capture different types of relationships simultaneously.
- Positional Encoding: Sinusoidal or learned embeddings inject position information since the model has no inherent sense of order.
- Feed-Forward Layers: Applied pointwise after attention, providing nonlinear transformation.
- Layer Normalization and Residual Connections: Stabilize training.

The original Transformer was designed for machine translation using an encoder-decoder structure. Later variants like BERT (encoder-only) and GPT (decoder-only) adapted the architecture for different tasks.

Transformers have become the dominant architecture in NLP, and have since spread to computer vision (Vision Transformer, ViT), audio, reinforcement learning, and multimodal systems.

Key papers: "Attention Is All You Need" (2017), BERT (2018), GPT series (2018-2023).
""",
        "source_type": "text",
    },
    {
        "title": "Attention Mechanism in Deep Learning",
        "content": """
Attention mechanisms allow neural networks to dynamically focus on relevant parts of the input when producing each output element. Originally introduced for neural machine translation (Bahdanau et al., 2015), attention has become a foundational building block.

Types of attention:
- Additive (Bahdanau) Attention: Uses a small feed-forward network to compute alignment scores.
- Scaled Dot-Product Attention: Computes Q·K^T / sqrt(d_k), then softmax to get weights applied to V. Used in Transformers.
- Self-Attention (Intra-Attention): Relates positions within a single sequence to each other.
- Cross-Attention: Query comes from one sequence, keys/values from another (e.g. encoder-decoder).

Mathematical formulation:
  Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) · V

The scaling factor sqrt(d_k) prevents extremely small gradients when d_k is large.

Multi-Head Attention runs h parallel attention functions and concatenates results:
  MultiHead(Q, K, V) = Concat(head_1,...,head_h) · W_O

Attention has computational complexity O(n^2 * d) where n is sequence length, motivating efficient variants like Sparse Attention, Linformer, and Flash Attention.
""",
        "source_type": "text",
    },
    {
        "title": "Large Language Models Overview",
        "content": """
Large Language Models (LLMs) are neural networks trained on massive text corpora to model the probability distribution over text. They are typically based on the Transformer decoder architecture and trained via next-token prediction (causal language modeling).

Scale and training:
- GPT-3 (2020): 175B parameters, trained on ~300B tokens.
- PaLM (2022): 540B parameters.
- LLaMA 2 (2023): Open weights, 7B-70B parameters.
- GPT-4 (2023): Estimated ~1T parameters, multimodal.

Emergent capabilities: As LLMs scale, they exhibit emergent abilities not seen in smaller models, such as few-shot learning, chain-of-thought reasoning, and code generation.

Training pipeline:
1. Pretraining on large text corpus (self-supervised)
2. Supervised Fine-Tuning (SFT) on instruction-following data
3. RLHF (Reinforcement Learning from Human Feedback) to align behavior

Inference: LLMs are autoregressive — they generate tokens one at a time, with each new token conditioned on all prior tokens. Techniques like beam search, temperature sampling, and top-p (nucleus) sampling control generation quality and diversity.

Key challenges: hallucination, context window limits, computational cost, bias, and safety alignment.
""",
        "source_type": "text",
    },
    {
        "title": "Gradient Descent and Optimization",
        "content": """
Gradient descent is the core optimization algorithm for training neural networks. Given a loss function L(θ), it iteratively updates parameters θ in the direction of the negative gradient.

Update rule: θ ← θ - η · ∇_θ L

Variants:
- Batch Gradient Descent: Uses the full dataset per update. Accurate but slow.
- Stochastic Gradient Descent (SGD): One sample per update. Noisy but fast.
- Mini-Batch SGD: Uses a batch of 32-512 samples. Standard in practice.

Adaptive optimizers:
- AdaGrad: Adapts learning rate per parameter using accumulated squared gradients.
- RMSProp: Uses exponential moving average of squared gradients.
- Adam (Adaptive Moment Estimation): Combines momentum and RMSProp. Most widely used optimizer. Maintains first and second moment estimates.

Learning rate scheduling: Constant LR rarely optimal. Common schedules: cosine annealing, linear warmup + decay, OneCycleLR.

Challenges: saddle points, vanishing/exploding gradients, local minima, ill-conditioning. Techniques like gradient clipping, batch normalization, and careful initialization help.

In deep learning, second-order methods (Newton's method, L-BFGS) are rarely used due to prohibitive memory and compute cost at scale.
""",
        "source_type": "text",
    },
    {
        "title": "Convolutional Neural Networks",
        "content": """
Convolutional Neural Networks (CNNs) are a class of deep learning models designed for grid-structured data such as images. They use local connectivity and weight sharing via convolutional filters to learn spatial hierarchies of features.

Core components:
- Convolutional Layer: Applies learned filters across spatial dimensions. Produces feature maps capturing local patterns.
- Activation Function: ReLU (Rectified Linear Unit) applied after convolution: f(x) = max(0, x).
- Pooling Layer: Reduces spatial dimensions (max pool, average pool). Provides translational invariance.
- Fully Connected Layer: Final layers aggregate features for classification or regression.

Key architectural innovations:
- AlexNet (2012): First deep CNN to win ImageNet. Used ReLU, dropout.
- VGG (2014): Very deep networks with 3x3 filters only.
- ResNet (2015): Skip connections (residual connections) allow training of 100+ layer networks.
- EfficientNet (2019): Compound scaling of depth, width, resolution.

Applications: image classification, object detection (YOLO, Faster R-CNN), semantic segmentation, face recognition, medical imaging.

Limitations vs Transformers: CNNs have limited global receptive field unless very deep. Vision Transformers (ViT) have challenged CNN dominance by applying self-attention directly to image patches.
""",
        "source_type": "text",
    },
    {
        "title": "Reinforcement Learning Fundamentals",
        "content": """
Reinforcement Learning (RL) is a framework where an agent learns to take actions in an environment to maximize cumulative reward. Unlike supervised learning, there is no labeled dataset — the agent discovers good behavior through trial and error.

Key concepts:
- Agent: The learner/decision-maker.
- Environment: What the agent interacts with.
- State (s): Current situation.
- Action (a): What the agent can do.
- Reward (r): Scalar feedback signal.
- Policy (π): Mapping from states to actions. The goal is to find the optimal policy.
- Value Function V(s): Expected cumulative reward from state s.
- Q-Function Q(s,a): Expected cumulative reward from taking action a in state s.

Algorithms:
- Q-Learning: Model-free, off-policy. Bellman equation: Q(s,a) ← r + γ max_a' Q(s',a')
- Deep Q-Network (DQN): Uses a neural network to approximate Q-function. DeepMind's Atari breakthrough.
- Policy Gradient: Directly optimize the policy. REINFORCE algorithm.
- Actor-Critic: Combines policy gradient with value function estimation.
- Proximal Policy Optimization (PPO): Stable, widely-used policy gradient method.

Applications: game playing (AlphaGo, Atari), robotic control, autonomous driving, RLHF for LLM alignment.

Challenges: sample efficiency, sparse rewards, credit assignment, exploration vs exploitation.
""",
        "source_type": "text",
    },
]


def main():
    print("Seeding knowledge base with foundational AI/ML articles...\n")
    for article in SEED_ARTICLES:
        save_source(
            title=article["title"],
            content=article["content"].strip(),
            source_type=article["source_type"],
        )
    print(f"\n✓ Seeded {len(SEED_ARTICLES)} articles into raw/")
    print("Next step: run  python compile_wiki.py  to compile the wiki")


if __name__ == "__main__":
    main()
