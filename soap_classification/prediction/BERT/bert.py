import torch
import pandas as pd
from tqdm import tqdm
from transformers import BertJapaneseTokenizer
from torch.utils.data import TensorDataset, random_split
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import BertForSequenceClassification, AdamW, BertConfig

# GPUが使えれば利用する設定
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# データの読み込み
df = pd.read_csv("labeled_dataset.csv", header=None, names=["SOAP", "label"])
df = df.sample(frac=0.1, random_state=42)

soaps = df.SOAP.values[1:-1]
labels = df.label.values[1:-1]

# 1. BERT Tokenizerを用いて単語分割・IDへ変換
## Tokenizerの準備
tokenizer = BertJapaneseTokenizer.from_pretrained(
    "cl-tohoku/bert-base-japanese-whole-word-masking"
)

# 最大単語数の確認
max_len = []
# 1文づつ処理
for soap in soaps:
    # Tokenizeで分割
    token_words = tokenizer.tokenize(soap)
    # 文章数を取得してリストへ格納
    max_len.append(len(token_words))

import numpy as np

# Mapping dictionary
label_map = {"X": 0, "S": 1, "O": 2, "A": 3, "P": 4}

# Apply mapping to the labels array
labels = np.array([label_map[label] for label in labels])

input_ids = []
attention_masks = []

# 1文づつ処理
for soap in soaps:
    encoded_dict = tokenizer.encode_plus(
        soap,
        add_special_tokens=True,  # Special Tokenの追加
        max_length=512,  # 文章の長さを固定（Padding/Trancatinating）
        pad_to_max_length=True,  # PADDINGで埋める
        return_attention_mask=True,  # Attention maksの作成
        return_tensors="pt",  #  Pytorch tensorsで返す
    )

    # 単語IDを取得
    input_ids.append(encoded_dict["input_ids"])

    # Attention　maskの取得
    attention_masks.append(encoded_dict["attention_mask"])

# リストに入ったtensorを縦方向（dim=0）へ結合
input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)

# tensor型に変換
labels = torch.tensor(labels)

# データセットクラスの作成
dataset = TensorDataset(input_ids, attention_masks, labels)

# 80%地点のIDを取得
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

# データセットを分割
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# データローダーの作成
batch_size = 15

# 訓練データローダー
train_dataloader = DataLoader(
    train_dataset,
    sampler=RandomSampler(train_dataset),  # ランダムにデータを取得してバッチ化
    batch_size=batch_size,
)

# 検証データローダー
validation_dataloader = DataLoader(
    val_dataset,
    sampler=SequentialSampler(val_dataset),  # 順番にデータを取得してバッチ化
    batch_size=batch_size,
)

# BertForSequenceClassification 学習済みモデルのロード
model = BertForSequenceClassification.from_pretrained(
    "cl-tohoku/bert-base-japanese-whole-word-masking",  # 日本語Pre trainedモデルの指定
    num_labels=5,  # ラベル数（今回はBinaryなので2、数値を増やせばマルチラベルも対応可）
    output_attentions=False,  # アテンションベクトルを出力するか
    output_hidden_states=False,  # 隠れ層を出力するか
)

# モデルをGPUへ転送
model.cuda()

# 最適化手法の設定
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)


# 訓練パートの定義
def train(model, pbar):
    model.train()  # 訓練モードで実行
    train_loss = 0
    for (
        batch
    ) in train_dataloader:  # train_dataloaderはword_id, mask, labelを出力する点に注意
        b_input_ids = batch[0].to(device)
        b_input_mask = batch[1].to(device)
        b_labels = batch[2].to(device)
        optimizer.zero_grad()
        loss = model(
            b_input_ids,
            token_type_ids=None,
            attention_mask=b_input_mask,
            labels=b_labels,
        ).loss  # 戻り値とここを修正
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        train_loss += loss.item()
        pbar.update(1)
    return train_loss


# テストパートの定義
def validation(model, pbar):
    model.eval()  # 訓練モードをオフ
    val_loss = 0
    with torch.no_grad():  # 勾配を計算しない
        for batch in validation_dataloader:
            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            b_labels = batch[2].to(device)
            with torch.no_grad():
                loss = model(
                    b_input_ids,
                    token_type_ids=None,
                    attention_mask=b_input_mask,
                    labels=b_labels,
                ).loss  # 戻り値とここを修正
            val_loss += loss.item()
            pbar.update(1)
    return val_loss


# 学習の実行
max_epoch = 4
train_loss_ = []
test_loss_ = []

for epoch in range(max_epoch):
    # Train the model with progress bar
    print(f"Epoch {epoch + 1}/{max_epoch}")
    with tqdm(
        total=len(train_dataloader), desc=f"Epoch {epoch + 1}/{max_epoch}", unit="batch"
    ) as pbar:
        train_ = train(model, pbar)
        train_loss_.append(train_)

    # Test the model with progress bar
    with tqdm(
        total=len(validation_dataloader),
        desc=f"Epoch {epoch + 1}/{max_epoch}",
        unit="batch",
    ) as pbar:
        test_ = validation(model, pbar)
        test_loss_.append(test_)
