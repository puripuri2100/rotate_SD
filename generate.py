import click
import json
import datetime
import os
import torch
from diffusers import StableDiffusionPipeline
from torch import autocast
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()


DEVICE = "cuda"

def make_now_iso_str_and_file_str() -> tuple[str, str]:
    now = datetime.datetime.now()
    now_iso_str = now.isoformat(timespec='seconds')
    now_file_str = now.strftime('%Y%m%d-%H%M%S')
    return (now_iso_str, now_file_str)


def path_to_json(path:str) -> list:
    json_open = open(path, 'r')
    json_data = json.load(json_open)
    return json_data


def write_json_date(path:str, lst:list[object]):
    file = open(path, 'w')
    json.dump(lst, file, indent = 2, ensure_ascii=False)

def make_image_path(model: str, datetime_str: str, is_nsfw: bool) -> str:
    if is_nsfw:
        return f"{model}/nsfw/{datetime_str}_nsfw.png"
    else:
        return f"{model}/{datetime_str}.png"


def data_to_object(model: str, prompt: str, datetime_str: str, is_nsfw: bool, file_path) -> object:
    obj = {
        "prompt": prompt,
        "datetime": datetime_str,
        "is_nsfw": is_nsfw,
        "file_path": file_path
    }
    return obj


def generate_stable(is_nsfw: bool, prompt: str, json_data:list[object], n:int, width:int, height:int, seed:int, scale:float):
    STABLE_DIFFUSION_TOKEN = os.environ["STABLE_DIFFUSION_TOKEN"]
    json_data = path_to_json(json)
    MODEL_ID = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float32, use_auth_token=STABLE_DIFFUSION_TOKEN)
    pipe.to(DEVICE)
    MODEL = "stable"
    if isnsfw:
        def null_safety(images, **kwargs):
            return images, False
        pipe.safety_checker = null_safety
    with autocast(DEVICE):
        for i in range(n):
            (now_iso, now_file) = make_now_iso_str_and_file_str()
            file_path = make_image_path(MODEL, now_file, is_nsfw)
            image = pipe(
                prompt,
                width=width,
                height=height,
                seed=seed,
                scale=scale
            )["sample"][0]
            image.save(file_path)
            data = data_to_object(MODEL, prompt, now_iso, is_nsfw, file_path)
            json_data.append(data)
            print(f"Image Generated({i})")
    write_json_date(json, json_data)
    print("All Done")


def generate_waifu(is_nsfw: bool, prompt: str, json_data:list[object], n:int, width:int, height:int, seed:int, scale:float):
    json_data = path_to_json(json)
    MODEL_ID = "hakurei/waifu-diffusion"
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float32)
    pipe.to(DEVICE)
    MODEL = "waifu"
    if is_nsfw:
        def null_safety(images, **kwargs):
            return images, False
        pipe.safety_checker = null_safety
    with autocast(DEVICE):
        for i in range(1, n+1):
            (now_iso, now_file) = make_now_iso_str_and_file_str()
            file_path = make_image_path(MODEL, now_file, is_nsfw)
            image = pipe(
                prompt,
                width=width,
                height=height,
                seed=seed,
                scale=scale
            )["sample"][0]
            image.save(file_path)
            data = data_to_object(MODEL, prompt, now_iso, is_nsfw, file_path)
            json_data.append(data)
            print(f"Image Generated({i})")
    write_json_date(json, json_data)
    print("All Done")


@click.group()
def cli():
    pass

@cli.command()
@click.option("--nsfw", required=False, is_flag=True, help="NSFW画像かどうかのフラグ")
@click.option("-p", "--prompt", required=True, help="生成に使われる説明文")
@click.option("-j", "--json", required=True, type=click.Path(), help="生成画像の記録を残してあるJSONファイルへのpath")
@click.option("-n", default=1, type=int, help="入力したpromptを使って何枚生成するか")
@click.option("-w", "--width", default=360, type=int, help="生成される画像の横幅px")
@click.option("-h", "--height", default=360, type=int, help="生成される画像の縦幅px")
@click.option("--seed", type=int, help="seed値")
@click.option("--scale", default=7.5, type=float, help="スケール")
def stable(nsfw, prompt, json, n, width, height, seed, scale):
    json_data = path_to_json(json)
    generate_stable(nsfw, prompt, json_data, n, width, height, seed, scale)


@cli.command()
@click.option("--nsfw", required=False, is_flag=True, help="NSFW画像かどうかのフラグ")
@click.option("-p", "--prompt", required=True, help="生成に使われる説明文")
@click.option("-j", "--json", required=True, type=click.Path(), help="生成画像の記録を残してあるJSONファイルへのpath")
@click.option("-n", default=1, type=int, help="入力したpromptを使って何枚生成するか")
@click.option("-w", "--width", default=320, type=int, help="生成される画像の横幅px")
@click.option("-h", "--height", default=320, type=int, help="生成される画像の縦幅px")
@click.option("--seed", type=int, help="seed値")
@click.option("--scale", default=7.5, type=float, help="スケール")
def waifu(nsfw, prompt, json, n, width, height, seed, scale):
    json_data = path_to_json(json)
    generate_waifu(nsfw, prompt, json_data, n, width, height, seed, scale)



if __name__ == "__main__":
    cli()
