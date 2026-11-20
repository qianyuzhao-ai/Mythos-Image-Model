from pathlib import Path

from PIL import Image
from mflux.models.common.training.state.training_spec import TrainingSpec


def check_smoke(config: Path) -> None:
    spec = TrainingSpec.resolve(config_path=str(config), resume_path=None, create_output_dir=False)
    if len(spec.data) != 4:
        raise ValueError(f"本次试训需要 4 张图片，当前读到 {len(spec.data)} 张。")

    stems = {item.image.stem for item in spec.data}
    if len(stems) != len(spec.data):
        raise ValueError("有多张图片共用同一个标注文件。请给每张图片取独立的文件名。")

    for item in spec.data:
        if item.input_image is not None:
            raise ValueError("本次试训使用文生图配对，请使用 01 至 04 这样的普通文件名。")
        caption = item.prompt.strip()
        if not caption.startswith("mythoscine") or not caption.removeprefix("mythoscine").strip(" \t\n，,。"):
            raise ValueError(f"请在 {item.image.with_suffix('.txt').name} 里用 mythoscine 开头，并写出实际画面。")
        with Image.open(item.image) as image:
            image.load()
            print(f"{item.image.name}  {image.width} × {image.height}  {caption}")


if __name__ == "__main__":
    try:
        check_smoke(Path(__file__).resolve().parents[1] / "configs" / "smoke.json")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error))
    print("4 组图片和标注均已读入。")
