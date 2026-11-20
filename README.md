# Mythos-Image-Model

神话图像模型，基于 Qwen Image 2.1 微调

## 在 Mac 上跑第一次试训

项目使用 Python 3.12、MLX 和 MFLUX。PyCharm 解释器选项目的 `.venv/bin/python`，下面的命令均从仓库根目录执行。基础权重放在 `models/Qwen-Image-2.1/`。配置中的 `model_path` 从工作目录解析，图片目录 `data` 从配置文件所在目录解析。

1. 把 4 张图放进 `data/smoke/`，文件名可用 `01.jpg` 至 `04.jpg`。每张配一份同名的 UTF-8 文本，如 `01.txt`。具体写法见[标注指南](data/标注指南.md)。
2. 运行以下命令检查图片和标注。它会打印训练器实际读到的文件名、尺寸和文字。

   ```sh
   .venv/bin/python scripts/check_smoke.py
   ```

3. 核对这四行内容后，在同一个终端使用项目里的权重离线启动试训。

   ```sh
   HF_HUB_OFFLINE=1 .venv/bin/mflux-train --config configs/smoke.json
   ```

[试训配置](configs/smoke.json)使用 Qwen-Image-2.1 基础版、512 分辨率、每批 1 张、共 5 轮。4 张图会更新 20 步。打开 `runs/smoke/preview/` 比较起点与第 20 步的样图。对应训练存档在 `runs/smoke/checkpoints/0000020_checkpoint.zip`，其中 `0000020_adapter.safetensors` 是可加载的 LoRA。已有同名运行目录时，MFLUX 会为新目录追加时间戳。

正式训练的选图与验收标准见[项目方案](项目方案.md)。

## 在新检出的项目中恢复环境

用 `uv sync --locked` 安装锁定的依赖，然后从仓库根目录运行下列命令，将同一版本的基础权重下载到本项目。模型文件约 33 GB。[官方模型文件](https://huggingface.co/Qwen/Qwen-Image-2.1/tree/d26bb61231c349cf6b7896fa83353113880e1ba3)

```sh
.venv/bin/hf download Qwen/Qwen-Image-2.1 \
  --revision d26bb61231c349cf6b7896fa83353113880e1ba3 \
  --local-dir models/Qwen-Image-2.1 --exclude 'assets/*'
```
