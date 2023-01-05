import requests
import json

cookies = {
    'ngenix_jscv_cd881f1695eb': 'cookie_expires=1672941290&cookie_signature=%2BRrw%2BCZihvzjhfZDG2IPQuryBts%3D',
    'external_analytics_anonymous_id': '82e17ace-4b24-4d71-8d2e-072b77daa797',
    'city_info': '%7B%22slug%22%3A%22omsk%22%2C%22name%22%3A%22%D0%9E%D0%BC%D1%81%D0%BA%22%2C%22lat%22%3A54.9978%2C%22lon%22%3A73.4001%7D',
    'rl_page_init_referrer': 'RudderEncrypt%3AU2FsdGVkX19JlGzXPc8ROJ12giUHisx0I0xSQCXt25vyOxvavwdKICLpqOlKID9l',
    'rl_page_init_referring_domain': 'RudderEncrypt%3AU2FsdGVkX19E3eOxlcInNrB4YFFrsXos7w%2FOpRkWSc8%3D',
    'mindboxDeviceUUID': '68745f96-1db3-4a5e-ac4f-524f08402c66',
    'directCrm-session': '%7B%22deviceGuid%22%3A%2268745f96-1db3-4a5e-ac4f-524f08402c66%22%7D',
    'sessionId': '16729376934012563400',
    '_pk_id.6.3ec0': 'dd7204700364021d.1672937694.',
    '_pk_ses.6.3ec0': '1',
    '_sa': 'SA1.46b683b3-1788-4cd7-8dfc-8e776532b139.1672937693',
    '_ym_uid': '1672937694102468340',
    '_ym_d': '1672937694',
    'iap.uid': 'c0c404dd129c490584baa95fc7071a0f',
    '_ym_isad': '2',
    'adtech_uid': '86d3bf52-6c18-4c9a-91c6-ffda5c2abbcb%3Asbermarket.ru',
    'top100_id': 't1.7588506.1939644089.1672937693771',
    'rrpvid': '762954941580069',
    'adrdel': '1',
    '_ym_visorc': 'b',
    'tmr_lvid': '8d6a567549907252b5010e0ad5124789',
    'tmr_lvidTS': '1672937694022',
    'adrcid': 'ApL45unfB7vKCyph6QnLSjg',
    'rcuid': '63b700de9562c1e4a1c2c6b9',
    'flocktory-uuid': 'e19c6de4-1e7c-4104-94e2-7d3d4eba20a0-8',
    'identified_address': 'true',
    'ssrMedia': '{%22windowWidth%22:880%2C%22primaryInput%22:%22mouse%22}',
    'rl_group_id': 'RudderEncrypt%3AU2FsdGVkX1%2Bm96ZgWUUrmxxgOZTy6XfS%2BgDrs5WjjQs%3D',
    'rl_group_trait': 'RudderEncrypt%3AU2FsdGVkX1%2BhfRBplYkIaZsKus%2BXsKly7n3sXp0g2n4%3D',
    'rl_anonymous_id': 'RudderEncrypt%3AU2FsdGVkX1%2FNfnDIaX6PbrlooKHXXxWi%2FkRwK253jz4PN9Dc4dLCKFcMer230yKCfz%2FFp%2B973%2Bcr5YU62UGGYQ%3D%3D',
    '_808db7ba1248': '%5B%7B%22source%22%3A%22sbermarket.ru%22%2C%22medium%22%3A%22referral%22%2C%22cookie_changed_at%22%3A1672938352%7D%2C%7B%22source%22%3A%22%28direct%29%22%2C%22medium%22%3A%22%28none%29%22%2C%22cookie_changed_at%22%3A1672938353%7D%5D',
    'last_visit': '1672916753498%3A%3A1672938353498',
    'rr-testCookie': 'testvalue',
    'rl_user_id': 'RudderEncrypt%3AU2FsdGVkX19wOpoBS7PUtiiIjo%2BUP%2BFWTh456FuMxyo%3D',
    'rl_trait': 'RudderEncrypt%3AU2FsdGVkX1%2Bt9xoWQiJdOCRO465TdevbxJazJ7bbKTX%2BidcdWC8gDJcTkFj5lRPohUKCmfBQiSdaB8%2FPgFRiqkYL3d7jhRN7xBSBA%2FGYm032rWHHlTZEAyhHNiE9pzSG1DpQ4qjVuo%2BA1yF6pb50dIx8zl0uEKkMW0ujAqZ7UpfChfq9TWDnypBRuUuoMr%2B2MMaAErJ6rjsRWMCL9hhv9mbd2dZTeZDz1GMi5JbLeuxLcoMY9PeYy4goqG%2BF3nOQAyQ7nuf3G4C6P8HjwpTczibp5U8HswhiE1M2RurTSRQPBTSBYqD4QzAV7S8GhZryD%2BbZz1VFHfSoa%2BHPzHZnodb1J7uDCR1dLBbUfdM4Nmo%3D',
    '_Instamart_session': 'eENVUUpoNEpjeEpzWE5ObWM4eU51ZXpQdHc4cVlkaDhmNHB1VnRZM29Gd3dYMWRzWUtpRlowYXplVE9EOHF0NXdXUjk1aWdwUWsyWkVnNHVad3NWVXRpaEdnTTk5bDVEc0dLZDFJZ3ozY3VrQStvdXYzWDhLcEY1SnBIT2dsdzBWOHR4c3lONmx6YVptbEYvcUlJejltT08rS1RicmpqVmk1VXIyWlEvaWRBUDBvbDNjcEJJeDJxSHFOV1ROOGt4L3ZYV2VJUU5BVWhmTEdiNTFTT1N6dz09LS1ib1UzMmdSdERkNTlBRDNBTDFlZXRnPT0%3D--daab70f2f0f65c063f09a68dbea1bfebd2bd7e6d',
    'tmr_detect': '0%7C1672938355888',
    't3_sid_7588506': 's1.180638995.1672937693778.1672938358509.1.41',
    'rl_session': 'RudderEncrypt%3AU2FsdGVkX1%2Bf%2Ba9Abn97gcGCQBhl2%2BvbU0DTyjMNShCxUFNECjVTp8uudhB0qUG%2BDmoTYIMtekyHpByn6%2FuJIFOTEBV38sDLjttwWavd3GzhKs1D7VIZHujM3QnkVOKb2GWRLNXBQvK9qLPpFe6tBg%3D%3D',
}

headers = {
    'authority': 'sbermarket.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en;q=0.9',
    'api-version': '3.0',
    'cache-control': 'no-cache',
    'client-token': '7ba97b6f4049436dab90c789f946ee2f',
    # 'cookie': 'ngenix_jscv_cd881f1695eb=cookie_expires=1672941290&cookie_signature=%2BRrw%2BCZihvzjhfZDG2IPQuryBts%3D; external_analytics_anonymous_id=82e17ace-4b24-4d71-8d2e-072b77daa797; city_info=%7B%22slug%22%3A%22omsk%22%2C%22name%22%3A%22%D0%9E%D0%BC%D1%81%D0%BA%22%2C%22lat%22%3A54.9978%2C%22lon%22%3A73.4001%7D; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX19JlGzXPc8ROJ12giUHisx0I0xSQCXt25vyOxvavwdKICLpqOlKID9l; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX19E3eOxlcInNrB4YFFrsXos7w%2FOpRkWSc8%3D; mindboxDeviceUUID=68745f96-1db3-4a5e-ac4f-524f08402c66; directCrm-session=%7B%22deviceGuid%22%3A%2268745f96-1db3-4a5e-ac4f-524f08402c66%22%7D; sessionId=16729376934012563400; _pk_id.6.3ec0=dd7204700364021d.1672937694.; _pk_ses.6.3ec0=1; _sa=SA1.46b683b3-1788-4cd7-8dfc-8e776532b139.1672937693; _ym_uid=1672937694102468340; _ym_d=1672937694; iap.uid=c0c404dd129c490584baa95fc7071a0f; _ym_isad=2; adtech_uid=86d3bf52-6c18-4c9a-91c6-ffda5c2abbcb%3Asbermarket.ru; top100_id=t1.7588506.1939644089.1672937693771; rrpvid=762954941580069; adrdel=1; _ym_visorc=b; tmr_lvid=8d6a567549907252b5010e0ad5124789; tmr_lvidTS=1672937694022; adrcid=ApL45unfB7vKCyph6QnLSjg; rcuid=63b700de9562c1e4a1c2c6b9; flocktory-uuid=e19c6de4-1e7c-4104-94e2-7d3d4eba20a0-8; identified_address=true; ssrMedia={%22windowWidth%22:880%2C%22primaryInput%22:%22mouse%22}; rl_group_id=RudderEncrypt%3AU2FsdGVkX1%2Bm96ZgWUUrmxxgOZTy6XfS%2BgDrs5WjjQs%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2BhfRBplYkIaZsKus%2BXsKly7n3sXp0g2n4%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX1%2FNfnDIaX6PbrlooKHXXxWi%2FkRwK253jz4PN9Dc4dLCKFcMer230yKCfz%2FFp%2B973%2Bcr5YU62UGGYQ%3D%3D; _808db7ba1248=%5B%7B%22source%22%3A%22sbermarket.ru%22%2C%22medium%22%3A%22referral%22%2C%22cookie_changed_at%22%3A1672938352%7D%2C%7B%22source%22%3A%22%28direct%29%22%2C%22medium%22%3A%22%28none%29%22%2C%22cookie_changed_at%22%3A1672938353%7D%5D; last_visit=1672916753498%3A%3A1672938353498; rr-testCookie=testvalue; rl_user_id=RudderEncrypt%3AU2FsdGVkX19wOpoBS7PUtiiIjo%2BUP%2BFWTh456FuMxyo%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2Bt9xoWQiJdOCRO465TdevbxJazJ7bbKTX%2BidcdWC8gDJcTkFj5lRPohUKCmfBQiSdaB8%2FPgFRiqkYL3d7jhRN7xBSBA%2FGYm032rWHHlTZEAyhHNiE9pzSG1DpQ4qjVuo%2BA1yF6pb50dIx8zl0uEKkMW0ujAqZ7UpfChfq9TWDnypBRuUuoMr%2B2MMaAErJ6rjsRWMCL9hhv9mbd2dZTeZDz1GMi5JbLeuxLcoMY9PeYy4goqG%2BF3nOQAyQ7nuf3G4C6P8HjwpTczibp5U8HswhiE1M2RurTSRQPBTSBYqD4QzAV7S8GhZryD%2BbZz1VFHfSoa%2BHPzHZnodb1J7uDCR1dLBbUfdM4Nmo%3D; _Instamart_session=eENVUUpoNEpjeEpzWE5ObWM4eU51ZXpQdHc4cVlkaDhmNHB1VnRZM29Gd3dYMWRzWUtpRlowYXplVE9EOHF0NXdXUjk1aWdwUWsyWkVnNHVad3NWVXRpaEdnTTk5bDVEc0dLZDFJZ3ozY3VrQStvdXYzWDhLcEY1SnBIT2dsdzBWOHR4c3lONmx6YVptbEYvcUlJejltT08rS1RicmpqVmk1VXIyWlEvaWRBUDBvbDNjcEJJeDJxSHFOV1ROOGt4L3ZYV2VJUU5BVWhmTEdiNTFTT1N6dz09LS1ib1UzMmdSdERkNTlBRDNBTDFlZXRnPT0%3D--daab70f2f0f65c063f09a68dbea1bfebd2bd7e6d; tmr_detect=0%7C1672938355888; t3_sid_7588506=s1.180638995.1672937693778.1672938358509.1.41; rl_session=RudderEncrypt%3AU2FsdGVkX1%2Bf%2Ba9Abn97gcGCQBhl2%2BvbU0DTyjMNShCxUFNECjVTp8uudhB0qUG%2BDmoTYIMtekyHpByn6%2FuJIFOTEBV38sDLjttwWavd3GzhKs1D7VIZHujM3QnkVOKb2GWRLNXBQvK9qLPpFe6tBg%3D%3D',
    'is-storefront-ssr': 'false',
    'pragma': 'no-cache',
    'referer': 'https://sbermarket.ru/lenta/c/priedlozhieniia/skidki/ovoshchi-frukti-orekhi?sid=699&source=category',
    'sec-ch-ua': '"Chromium";v="106", "Yandex";v="22", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36',
}

params = {
    'tid': 'priedlozhieniia/skidki/ovoshchi-frukti-orekhi',
    'page': '2',
    'per_page': '20',
    'sort': 'popularity',
}

response = requests.get('https://sbermarket.ru/api/v3/stores/699/products', params=params, cookies=cookies, headers=headers)

with open("mywork/Tests/test.json", 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, indent=4, ensure_ascii=False)