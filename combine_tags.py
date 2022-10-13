import PySimpleGUI as sg
import generate
import random
import statistics



def tag_to_str_with_weights(tag: str, weights: list[int]):
    plus_lst = list(filter(lambda x: x > 0, weights))
    if len(plus_lst) == 0:
        plus_mean = 0
    else:
        plus_mean = statistics.mean(plus_lst)
    minus_lst = list(filter(lambda x: x < 0, weights))
    if len(minus_lst) == 0:
        minus_mean = 0
    else:
        minus_mean = statistics.mean(minus_lst)
    zero_lst = list(filter(lambda x: x == 0, weights))
    if len(zero_lst) > len(plus_lst) + len(minus_lst):
        # どちらとも評価しがたいため、そのまま出力
        return tag
    elif plus_mean + minus_mean < 2.0:
        # プラスの評価とマイナスの評価が拮抗している
        return "({" + tag + "})"
    elif plus_mean > 8.0:
        if plus_mean > minus_mean * -1.5:
            # とても良い評価なのでとても強調
            return "{{{{{{" + tag + "}}}}}}"
        else:
            # 良い評価なので強調
            return "{{{{{" + tag + "}}}}}"
    elif plus_mean > 6.0:
        if plus_mean > minus_mean * -2.0:
            return "{{{{{" + tag + "}}}}}"
        elif plus_mean > minus_mean * -1.5:
            return "{{{{" + tag + "}}}}"
        else:
            return "{{{" + tag + "}}}"
    elif plus_mean > 3.0:
        if plus_mean > minus_mean * -1.5:
            return "{{{" + tag + "}}}"
        else:
            return "{{" + tag + "}}"

    elif minus_mean < -9.0 :
        # あまりにも評価が悪いため、排除
        return None
    elif minus_mean < -6.0 :
        if minus_mean > plus_mean * -2.0:
            return "((((" + tag + "))))"
        elif minus_mean > plus_mean * -1.5:
            return "(((" + tag + ")))"
        else:
            return "((" + tag + "))"
    elif minus_mean < -3.0 :
        if minus_mean > plus_mean * -1.5:
            return "((" + tag + "))"
        else:
            return "(" + tag + ")"

    else:
        return tag


def choice_tags(n: int, tags: list[object], data_json: object, is_weighting: bool) -> list[str]:
    lst = []
    tag_lst_len = len(tags)
    for j in range(n):
        i = random.randrange(tag_lst_len)
        tag = tags[i]["tag"]
        weights = data_json.get(tag)
        if weights == None or (not is_weighting):
            lst.append((tag, tag))
        else:
            tag_str = tag_to_str_with_weights(tag, weights)
            if tag_str != None:
                lst.append((tag, tag_str))
    return lst


def generate_prompt(data_json, tags_json, is_weighting, is_nsfw):
    use_tag_lst = []
    prompt_str_lst = []
    body_data = tags_json["body"]
    face_tags = body_data["face"]
    eyes_tags = body_data["eyes"]
    ears_tags = body_data["ears"]
    hair_tags = body_data["hair"]
    breasts_tags = body_data["breasts"]
    wings_tags = body_data["wings"]
    tail_tags = body_data["tail"]
    body_others_tags = body_data["others"]
    attire_tags = tags_json["attire"]
    objects_tags = tags_json["objects"]
    descriptions_tags = tags_json["descriptions"]
    others_tags = tags_json["others"]
    # 顔の情報
    # とりあえずランダムで2要素を選択
    for (tag_str, prompt_str) in choice_tags(2, face_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # 目の情報
    for (tag_str, prompt_str) in choice_tags(2, eyes_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # 耳の情報
    for (tag_str, prompt_str) in choice_tags(1, ears_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # 髪の情報
    for (tag_str, prompt_str) in choice_tags(4, hair_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # 胸の情報
    for (tag_str, prompt_str) in choice_tags(2, breasts_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # 羽の情報
    # 要らない場合もあるので調節
    # とりあえず2割
    if random.random() < 0.2:
        for (tag_str, prompt_str) in choice_tags(1, wings_tags, data_json, is_weighting):
            use_tag_lst.append(tag_str)
            use_tag_lst.append(prompt_str)
    # しっぽの情報
    # 要らない場合もあるので調節
    # とりあえず2割
    if random.random() < 0.2:
        for (tag_str, prompt_str) in choice_tags(1, tail_tags, data_json, is_weighting):
            use_tag_lst.append(tag_str)
            use_tag_lst.append(prompt_str)
    # 身体関係のその他の情報
    for (tag_str, prompt_str) in choice_tags(5, body_others_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # 服の情報
    for (tag_str, prompt_str) in choice_tags(3, attire_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # 物の情報
    for (tag_str, prompt_str) in choice_tags(3, objects_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # 主観情報など
    for (tag_str, prompt_str) in choice_tags(3, descriptions_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)
    # その他の情報など
    for (tag_str, prompt_str) in choice_tags(3, others_tags, data_json, is_weighting):
        use_tag_lst.append(tag_str)
        use_tag_lst.append(prompt_str)

    if is_nsfw:
        nsfw_tags = tags_json["nsfw"]
        # NSFW要素
        for (tag_str, prompt_str) in choice_tags(10, nsfw_tags, data_json, is_weighting):
            use_tag_lst.append(tag_str)
            use_tag_lst.append(prompt_str)

    prompt = ", ".join(prompt_str_lst)
    return (use_tag_lst, prompt)

# ウィンドウのレイアウト
layout = [
        [sg.Text("結果保存用jsonのpath"), sg.Input(key="-json_path-")],
        [sg.Text(key="-json_path_input_box_msg-")],
        [sg.Text("タグデータjsonのpath"), sg.Input("danbooru_tags.json", key="-tags_path-")],
        [sg.Text(key="-tags_path_input_box_msg-")],
        [sg.Text("出力dir"), sg.Input(key="-output_dir-")],
        [sg.Text(key="-output_dir_input_box_msg-")],
        #[
        #    sg.Text("画像生成のモデル"),
        #    sg.Radio("Waifu Diffusion", "-model-", key="-model_waifu-"),
        #    sg.Radio("NovelAI Diffusion", "-model-", key="-model_novelai-")
        #],
        #[sg.Text(key="-model_input_box_msg-")],
        [sg.Text("NSFW?"), sg.Checkbox("NSFW", key="-is_nsfw-", default=True)],
        [sg.Text("重みづけを有効化するか？"), sg.Checkbox("有効", key="-is_weighting-", default=True)],
        [sg.Text("追加のprompt"), sg.Multiline(key="-add_prompt-", size=(None, 8), font=(None, 10))],
        [sg.Button("生成", key="-generate-"), sg.Text("", key="-generate_log_msg-")],
        [sg.Text("生成文字列"), sg.InputText("", key="-generate_prompt_str-")],
        [sg.Image(key="-generate_image-")],
        [sg.Text("好み度合")],
        [sg.Slider(
            range=(-10, 10),
            default_value=0,
            resolution=1,
            orientation='h',
            enable_events=True,
            key="-likes_slider-"
        )],
        [
            sg.InputText(
                0,
                key="-likes_input_box-"
            ),
            sg.Button("登録", key="-register-"),
            sg.Text("", key="-likes_input_box_msg-")
        ],
    ]


# ウィンドウオブジェクトの作成
window = sg.Window("Combine Tags", layout)

used_tag_lst = []
is_generated = False
tags_json_path_tmp = ""
tags_data = {}

while True:
    # イベントの読み込み
    event, values = window.read()
    # ウィンドウの×ボタンが押されれば終了
    if event == sg.WIN_CLOSED:
        break
    else:
        if event == "-generate-":
            is_generate_ok = True
            # JSONファイルのpath
            if values["-json_path-"] == "":
                window["-json_path_input_box_msg-"].update(f"ログ用JSONファイルのpathは必ず入力してください", text_color="yellow")
                is_generate_ok = False
            else:
                window["-json_path_input_box_msg-"].update("")
            # タグデータJSONファイルのpath
            if values["-tags_path-"] == "":
                window["-tags_path_input_box_msg-"].update(f"タグデータjsonファイルのpathは必ず入力してください", text_color="yellow")
                is_generate_ok = False
            else:
                window["-tags_path_input_box_msg-"].update("")
            # 画像出力先
            if values["-output_dir-"] == "":
                window["-output_dir_input_box_msg-"].update(f"結果保存用jsonファイルのpathは必ず入力してください", text_color="yellow")
                is_generate_ok = False
            else:
                window["-output_dir_input_box_msg-"].update("")

            # 画像の生成
            if is_generate_ok:
                try:
                    is_nsfw = values["-is_nsfw-"]
                    seed = random.randint(0, 2**32 - 1)
                    (_, now_str) = generate.make_now_iso_str_and_file_str()
                    output_dir = values["-output_dir-"]
                    file_path = f"{output_dir}/{now_str}_{seed}.png"
                    json_path = values["-json_path-"]
                    data_json = generate.path_to_json(json_path)
                    tags_json_path = values["-tags_path-"]
                    if tags_json_path_tmp != tags_json_path:
                        print("タグデータ読み込み中")
                        tags_json = generate.path_to_json(tags_json_path)
                    is_weighting = values["-is_weighting-"]
                    (tags, prompt) = generate_prompt(data_json, tags_json, is_weighting, is_nsfw)
                    prompt = "{{{{masterpiece}}}}, UnrealEngine, 4K, 8K, " + prompt + values["-add_prompt-"]
                    generate.generate_waifu(True, prompt, [], 1, 320, 320, seed, 7.5, file_path)
                    window["-generate_image-"].update(filename=file_path)
                    used_tag_lst = tags
                    window["-generate_log_msg-"].update("生成成功", text_color="blue")
                    window["-generate_prompt_str-"].update(prompt)
                    window["-likes_input_box_msg-"].update("")
                    is_generated = True
                except:
                    window["-generate_log_msg-"].update("生成失敗", text_color="red")
                    is_generated = False

        # スライドバーの反映
        if event == "-likes_slider-":
            window["-likes_input_box-"].update(int(values["-likes_slider-"]))

        # 好み度合いの登録
        if event == "-register-":
            try:
                like_value = int(values["-likes_input_box-"])
                window["-likes_slider-"].update(like_value)
            except:
                window["-likes_input_box_msg-"].update("好み度合いは整数で与えてください")
            if is_generated:
                is_register_ok = True
                # JSONファイルのpath
                if values["-json_path-"] == "":
                    window["-json_path_input_box_msg-"].update(f"ログ用JSONファイルのpathは必ず入力してください", text_color="yellow")
                    is_generate_ok = False
                else:
                    window["-json_path_input_box_msg-"].update("")
                if is_register_ok:
                    try:
                        json_path = values["-json_path-"]
                        data_json = generate.path_to_json(json_path)
                        for tag in used_tag_lst:
                            like_value_lst = data_json.get(tag)
                            if like_value_lst == None:
                                like_value_lst = [like_value]
                            else:
                                like_value_lst.append(like_value)
                            data_json[tag] = like_value_lst
                        generate.write_json_date(json_path, data_json)
                        window["-likes_input_box_msg-"].update("登録成功", text_color="blue")
                        is_generated = False
                    except:
                        window["-likes_input_box_msg-"].update("登録失敗", text_color="red")



# ウィンドウ終了処理
window.close()



