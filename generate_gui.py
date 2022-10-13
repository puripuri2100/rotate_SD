import PySimpleGUI as sg
import generate



# ウィンドウのレイアウト
layout = [
        [sg.Text("ログ用JSONファイルのpath"), sg.Input(key="-json_path-")],
        [sg.Text(key="-json_path_input_box_msg-")],
        [
            sg.Text("画像生成のモデル"),
            sg.Radio("Stable Diffusion", "-model-", key="-model_stable-"),
            sg.Radio("Waifu Diffusion", "-model-", key="-model_waifu-")
        ],
        [sg.Text(key="-model_input_box_msg-")],
        [sg.Text("NSFW?"), sg.Checkbox("NSFW", key="-is_nsfw-")],
        [sg.Text("生成キーワード"), sg.Multiline(key="-prompt-", size=(None, 12), font=(None, 15))],
        [sg.Text(key="-prompt_input_box_msg-")],
        [sg.Text("オプション：")],
        [sg.Text("生成枚数(int)"), sg.Input(key="-generate_n-", default_text="1"), sg.Text(key="-generate_n_input_box_msg-")],
        [sg.Text("画像の横幅(int)"), sg.Input(key="-image_width-", default_text="320"), sg.Text(key="-image_width_input_box_msg-")],
        [sg.Text("画像の縦幅(int)"), sg.Input(key="-image_height-", default_text="320"), sg.Text(key="-image_height_input_box_msg-")],
        [sg.Text("seed値(int)"), sg.Input(key="-generate_seed_value-"), sg.Text(key="-generate_seed_value_input_box_msg-")],
        [sg.Text("scale(float)"), sg.Input(key="-generate_scale-", default_text="7.5"), sg.Text(key="-generate_scale_input_box_msg-")],
        [sg.Button("生成")],
        [sg.Text("", key="-generate_log_msg-")],
    ]


# ウィンドウオブジェクトの作成
window = sg.Window("Stable/Waifu Diffusion use with GUI", layout)


while True:
    # イベントの読み込み
    event, values = window.read()
    # ウィンドウの×ボタンが押されれば終了
    if event == sg.WIN_CLOSED:
        break
    if event == "生成":
        is_generate_ok = True
        # JSONファイルのpath
        if values["-json_path-"] == "":
            window["-json_path_input_box_msg-"].update(f"ログ用JSONファイルのpathは必ず入力してください", text_color="yellow")
            is_generate_ok = False
        else:
            window["-json_path_input_box_msg-"].update("")
        # 生成モデルの選択
        if not (values["-model_stable-"] or values["-model_waifu-"]):
            window["-model_input_box_msg-"].update(f"画像生成のモデルは必ず選択してください", text_color="yellow")
            is_generate_ok = False
        else:
            window["-model_input_box_msg-"].update("")
        # prompt
        if values["-prompt-"] == "":
            window["-prompt_input_box_msg-"].update(f"生成用キーワードは必ず入力してください", text_color="yellow")
            is_generate_ok = False
        else:
            window["-prompt_input_box_msg-"].update("")
            prompt = values["-prompt-"]
        # 生成枚数
        if values["-generate_n-"] == "":
            window["-generate_n_input_box_msg-"].update(f"生成枚数を入力してください", text_color="yellow")
            is_generate_ok = False
        else:
            try:
                int(values["-generate_n-"])
                window["-generate_n_input_box_msg-"].update("")
            except:
                window["-generate_n_input_box_msg-"].update(f"数字を入力してください", text_color="yellow")
                is_generate_ok = False
        # 画像の横幅
        if values["-image_width-"] == "":
            window["-image_width_input_box_msg-"].update(f"画像の横幅を入力してください", text_color="yellow")
            is_generate_ok = False
        else:
            try:
                int(values["-image_width-"])
                window["-image_width_input_box_msg-"].update("")
            except:
                window["-image_width_input_box_msg-"].update(f"数字を入力してください", text_color="yellow")
                is_generate_ok = False
        # 画像の縦幅
        if values["-image_height-"] == "":
            window["-image_height_input_box_msg-"].update(f"画像の縦幅を入力してください", text_color="yellow")
            is_generate_ok = False
        else:
            try:
                int(values["-image_height-"])
                window["-image_height_input_box_msg-"].update("")
            except:
                window["-image_height_input_box_msg-"].update(f"数字を入力してください", text_color="yellow")
                is_generate_ok = False
        # seed値
        if values["-generate_seed_value-"] == "":
            window["-generate_seed_value_input_box_msg-"].update("")
            generate_seed_value = None
        else:
            try:
                int(values["-generate_seed_value-"])
                window["-generate_seed_value_input_box_msg-"].update("")
                generate_seed_value = int(values["-generate_seed_value-"])
            except:
                window["-generate_seed_value_input_box_msg-"].update(f"数字を入力してください", text_color="yellow")
                is_generate_ok = False
        # scale
        if values["-generate_scale-"] == "":
            window["-generate_scale_input_box_msg-"].update(f"scaleを入力してください", text_color="yellow")
            is_generate_ok = False
        else:
            try:
                float(values["-generate_scale-"])
                window["-generate_scale_input_box_msg-"].update("")
            except:
                window["-generate_scale_input_box_msg-"].update(f"数字を入力してください", text_color="yellow")
                is_generate_ok = False
        if is_generate_ok:
            # 生成条件が整った場合にのみ生成を開始する
            is_err = False
            json_file_path = values["-json_path-"]
            is_nsfw = values["-is_nsfw-"]
            generate_n = int(values["-generate_n-"])
            width=int(values["-image_width-"])
            height=int(values["-image_height-"])
            scale=float(values["-generate_scale-"])
            json_data = generate.path_to_json(json_file_path)
            try:
                if values["-model_stable-"]:
                    generate.generate_stable(is_nsfw, prompt, json_data, generate_n, width, height, generate_seed_value, scale)
                elif values["-model_waifu-"]:
                    generate.generate_waifu(is_nsfw, prompt, json_data, generate_n, width, height, generate_seed_value, scale)
                else:
                    pass
                window["-generate_log_msg-"].update("All Done")
            except:
                window["-generate_log_msg-"].update("Err")


# ウィンドウ終了処理
window.close()
