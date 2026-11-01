import torch
import torch.nn as nn


class Simple1DCNN(nn.Module):
    """1D CNN regressor over the tabular distance/count feature vector.

    Treats the feature vector as a 1D signal (1 channel, length n_features)
    so that stacked Conv1d layers can learn local interactions between
    nearby distance/count columns (e.g. the three count bands of the same
    source) before pooling down to a single `pfas_sum` prediction.
    """

    def __init__(
        self,
        n_features: int,
        conv_channels: tuple[int, ...] = (32, 64, 64),
        kernel_size: int = 5,
        dropout: float = 0.2,
    ):
        super().__init__()

        conv_layers: list[nn.Module] = []
        in_channels = 1

        for out_channels in conv_channels:
            conv_layers += [
                nn.Conv1d(
                    in_channels,
                    out_channels,
                    kernel_size,
                    padding=kernel_size // 2,
                ),
                nn.BatchNorm1d(out_channels),
                nn.ReLU(),
                nn.MaxPool1d(2),
            ]
            in_channels = out_channels

        self.conv = nn.Sequential(*conv_layers)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_channels, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.unsqueeze(1)  # (batch, 1, n_features)
        x = self.conv(x)
        x = self.pool(x)
        return self.head(x).squeeze(-1)
