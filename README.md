# geetest
geetest点选验证码位置获取

# Demo
[点此查看识别结果](http://38.147.170.248:9990/geetest_click?image_url=https://static.geetest.com/captcha_v3/batch/v3/46335/2023-09-07T15/word/270a3da4a8eb4e66a014de56300073dd.jpg)
```json
{
  "coords":[
    [
      49,
      114.5
    ],
    [
      148.5,
      170
    ],
    [
      196,
      79.5
    ]
  ],
  "source":{
    "e":[
      164,
      48,
      228,
      111
    ],
    "发":[
      115,
      137,
      182,
      203
    ],
    "德":[
      14,
      80,
      84,
      149
    ]
  },
  "target":"德发长"
}
```

主要返回了3个字段
- target: 需要点击的文本.
- source: 待点击区域的文字识别以及坐标
- coords: 识别成功之后的需要点击的坐标