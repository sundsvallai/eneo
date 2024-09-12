# Changelog

## [1.1.1](https://github.com/inooLabs/intric-frontend/compare/intric/web@v1.1.0...intric/web@v1.1.1) (2024-08-27)


### Bug Fixes

* improve error handling for invalid/missing auth token ([80d0e63](https://github.com/inooLabs/intric-frontend/commit/80d0e6309456936fc6a8994d55e9c14de5fabcca))

## [1.1.0](https://github.com/inooLabs/intric-frontend/compare/intric/web@v1.0.2...intric/web@v1.1.0) (2024-08-19)


### Features

* add services to spaces ([#68](https://github.com/inooLabs/intric-frontend/issues/68)) ([23cd41a](https://github.com/inooLabs/intric-frontend/commit/23cd41a21c67096c8d109d55c6436b20726b8d10))
* show index info blobs for website crawls ([d1cfdd8](https://github.com/inooLabs/intric-frontend/commit/d1cfdd8125bb9112230321fd57c0c7d84dd6dfd3))


### Bug Fixes

* only allow knowledge selection of one embedding model at a time ([#66](https://github.com/inooLabs/intric-frontend/issues/66)) ([3107def](https://github.com/inooLabs/intric-frontend/commit/3107def85c1c6de57a2a1db6574be0b8dd349847))
* remove CORS config from front-end ([34d3633](https://github.com/inooLabs/intric-frontend/commit/34d3633ca739be1cfb0ca812cd34e0025fb6e75d))
* respect question's new lines in sessions ([36af1ee](https://github.com/inooLabs/intric-frontend/commit/36af1ee23d67ede3efd34dbc16ce34094d1e041b))
* show space selector in front of page header ([c75411c](https://github.com/inooLabs/intric-frontend/commit/c75411c9d5e48e5eefdda47dd49b5857d821b8b5))

## [1.0.2](https://github.com/inooLabs/intric-frontend/compare/intric/web@v1.0.1...intric/web@v1.0.2) (2024-08-08)


### Bug Fixes

* allow crawl type setting when creating a website ([dcf8816](https://github.com/inooLabs/intric-frontend/commit/dcf881656ad10553a52a0bf9b9a3bb98724123be))
* improve session handling when switching assistants ([#65](https://github.com/inooLabs/intric-frontend/issues/65)) ([ef620d0](https://github.com/inooLabs/intric-frontend/commit/ef620d0aeca27305d73e77981358f4af57f0ba59))
* page titles updated  ([#59](https://github.com/inooLabs/intric-frontend/issues/59)) ([3e2aa7c](https://github.com/inooLabs/intric-frontend/commit/3e2aa7c8bbac36ee96ee8d7012b3436057cf44c8))
* show "no options" hint in select menus ([#62](https://github.com/inooLabs/intric-frontend/issues/62)) ([586bed3](https://github.com/inooLabs/intric-frontend/commit/586bed392619c1113703bc53c6c842f427f4fcc9))
* show model names in knowledge selector ([#63](https://github.com/inooLabs/intric-frontend/issues/63)) ([e9216aa](https://github.com/inooLabs/intric-frontend/commit/e9216aaa61a2af032505b738ed660874c9367a14))

## [1.0.1](https://github.com/inooLabs/intric-frontend/compare/intric/web@v1.0.0...intric/web@v1.0.1) (2024-08-06)


### Bug Fixes

* redirect /assistants to /spaces/personal ([1283ecb](https://github.com/inooLabs/intric-frontend/commit/1283ecbfc7556f599a2a0ed42acc49867d2cdd1c))

## [1.0.0](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.28.0...intric/web@v1.0.0) (2024-08-05)


### ⚠ BREAKING CHANGES

* introduce workspaces
* remove legacy pages ([#52](https://github.com/inooLabs/intric-frontend/issues/52))

### Features

* add image upload to vision capable models ([#57](https://github.com/inooLabs/intric-frontend/issues/57)) ([ed7e809](https://github.com/inooLabs/intric-frontend/commit/ed7e809ff31960765211534d9d98c5779194734a))
* add knowledge to spaces ([#46](https://github.com/inooLabs/intric-frontend/issues/46)) ([7a23fd0](https://github.com/inooLabs/intric-frontend/commit/7a23fd06816e7aef100f945e2523254ea8106210))
* add members to spaces ([#48](https://github.com/inooLabs/intric-frontend/issues/48)) ([000ed6f](https://github.com/inooLabs/intric-frontend/commit/000ed6fe0c3d5aafdd28944c89d8fa272824911d))
* add personal space and tweaks ([#49](https://github.com/inooLabs/intric-frontend/issues/49)) ([d25d034](https://github.com/inooLabs/intric-frontend/commit/d25d03452b5f49e46a4173f65a6e0c91a5864c0d))
* add space overview table ([#52](https://github.com/inooLabs/intric-frontend/issues/52)) ([d51bfce](https://github.com/inooLabs/intric-frontend/commit/d51bfce577c6d906a886d813013658cdc7e16050))
* introduce workspaces ([5d4430d](https://github.com/inooLabs/intric-frontend/commit/5d4430d07d67eee61bb8b939fdef3b55802998a9))
* remove legacy pages ([#52](https://github.com/inooLabs/intric-frontend/issues/52)) ([d51bfce](https://github.com/inooLabs/intric-frontend/commit/d51bfce577c6d906a886d813013658cdc7e16050))
* resources can be moved between spaces ([#55](https://github.com/inooLabs/intric-frontend/issues/55)) ([713e48f](https://github.com/inooLabs/intric-frontend/commit/713e48f69ed274e8069fcc81d54934e95f39bd95))
* show used models in group and website table ([c656a89](https://github.com/inooLabs/intric-frontend/commit/c656a89910cd5d2e4bbccf31bc89cb602267fdda))
* spaces can have multiple embedding models ([#54](https://github.com/inooLabs/intric-frontend/issues/54)) ([8e953b5](https://github.com/inooLabs/intric-frontend/commit/8e953b528d3cc96563d712aaad8b4260c4941803))


### Bug Fixes

* allow scrolling on assistant and member list ([5c8b9c0](https://github.com/inooLabs/intric-frontend/commit/5c8b9c0e7127c9de6c028b3d73dba2774859dc60))
* hide member tile on personal space ([d7544b7](https://github.com/inooLabs/intric-frontend/commit/d7544b77ab1e4d986b7890670ab244a84d19bde2))
* implement permissions in personal space ([f713728](https://github.com/inooLabs/intric-frontend/commit/f713728a0a3e571ad3cadb616153be9978bae105))
* model label for vision ([#56](https://github.com/inooLabs/intric-frontend/issues/56)) ([7add198](https://github.com/inooLabs/intric-frontend/commit/7add1988297bb449a7c441a77f252b271b919fc7))
* move insights to admin ([#52](https://github.com/inooLabs/intric-frontend/issues/52)) ([d51bfce](https://github.com/inooLabs/intric-frontend/commit/d51bfce577c6d906a886d813013658cdc7e16050))
* some ui tweaks ([6aa4dc5](https://github.com/inooLabs/intric-frontend/commit/6aa4dc5e5dd68530c42a41e796d9252f8ce966ea))
* split personal space into its own menu item ([#52](https://github.com/inooLabs/intric-frontend/issues/52)) ([d51bfce](https://github.com/inooLabs/intric-frontend/commit/d51bfce577c6d906a886d813013658cdc7e16050))
* update wording on members page ([1427384](https://github.com/inooLabs/intric-frontend/commit/1427384f7ab4d19ac850b95be3342aa3b954415a))
* URL shortening for websites + new crawl status ([#51](https://github.com/inooLabs/intric-frontend/issues/51)) ([347ffae](https://github.com/inooLabs/intric-frontend/commit/347ffaedaede9a09c245e88083567eaf578f9869))

## [0.28.0](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.27.0...intric/web@v0.28.0) (2024-07-19)


### Features

* add assistants to spaces INTRC-245 ([#43](https://github.com/inooLabs/intric-frontend/issues/43)) ([c6f1d1d](https://github.com/inooLabs/intric-frontend/commit/c6f1d1d82575f9efa4d0b9746d1d21aa8f15ee5b))
* add settings to spaces ([#45](https://github.com/inooLabs/intric-frontend/issues/45)) ([3c9b57c](https://github.com/inooLabs/intric-frontend/commit/3c9b57c05a73ed165b6b1e9e5bd1b72388f6ea4a))


### Bug Fixes

* add completion model to assistant in spaces ([53cd874](https://github.com/inooLabs/intric-frontend/commit/53cd874e295d0878f53372d1b9558c047a3b953b))
* change creative model behaviour to a temperature of 1.25 ([e1bc808](https://github.com/inooLabs/intric-frontend/commit/e1bc80800aa14fee47a4b3cee165b8a8d9dc36da))
* only load websites when user has appropriate permissions ([3e60f87](https://github.com/inooLabs/intric-frontend/commit/3e60f87546ebff903a4b1553c740cdf8418739c7))

## [0.27.0](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.26.2...intric/web@v0.27.0) (2024-07-15)


### Features

* add sections on model page ([ce959f4](https://github.com/inooLabs/intric-frontend/commit/ce959f437be1a27b6bd116ac51201371cde7000a))
* add SpacesManager and SpaceSelector ([#41](https://github.com/inooLabs/intric-frontend/issues/41)) ([6300dd7](https://github.com/inooLabs/intric-frontend/commit/6300dd790a1c227accc08636946c13be6afef29a))
* move to new layout ([#38](https://github.com/inooLabs/intric-frontend/issues/38)) ([0d202db](https://github.com/inooLabs/intric-frontend/commit/0d202db5fd385d95bd04e36e59b2d1e29c5a44e0))


### Bug Fixes

* add aria labels to profile and notification buttons ([ba9a75f](https://github.com/inooLabs/intric-frontend/commit/ba9a75f45809912013546f6a77cb87d7079e4f48))
* rename "knowledge base" to "knowledge" ([de794b5](https://github.com/inooLabs/intric-frontend/commit/de794b508945e22b651f78696f376dcfe2f8e5e4))

## [0.26.2](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.26.1...intric/web@v0.26.2) (2024-07-05)


### Bug Fixes

* add logos to models ([0f3fb33](https://github.com/inooLabs/intric-frontend/commit/0f3fb3364fe060ab538e3de7f709b2bafc3ce123))
* remove model description placeholder ([1f3bd1b](https://github.com/inooLabs/intric-frontend/commit/1f3bd1b72dd34352bac6d611c31e536da37c3e31))
* unhide model cards ([a74f5c4](https://github.com/inooLabs/intric-frontend/commit/a74f5c44885d51131be08d12fef88a10659ca0ee))

## [0.26.1](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.26.0...intric/web@v0.26.1) (2024-07-04)


### Bug Fixes

* hide model cards ([f72d26e](https://github.com/inooLabs/intric-frontend/commit/f72d26ea12a9a58e65d889aba96ea78482d1c5b4))

## [0.26.0](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.25.0...intric/web@v0.26.0) (2024-07-04)


### Features

* add grid view/cards for models ([#32](https://github.com/inooLabs/intric-frontend/issues/32)) ([f39e927](https://github.com/inooLabs/intric-frontend/commit/f39e92756ee1267f025a784b611596b5c9781eef))
* add references component for links([#30](https://github.com/inooLabs/intric-frontend/issues/30)) ([c53e8e5](https://github.com/inooLabs/intric-frontend/commit/c53e8e599f3bac7d6708ca20b5c98c13d38d05d9))
* **intric/ui:** add labels component ([f39e927](https://github.com/inooLabs/intric-frontend/commit/f39e92756ee1267f025a784b611596b5c9781eef))

## [0.25.0](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.24.0...intric/web@v0.25.0) (2024-07-01)


### Features

* combine websites and collections into knowledge base INTRC-160 INTRC-165 ([#29](https://github.com/inooLabs/intric-frontend/issues/29)) ([a058415](https://github.com/inooLabs/intric-frontend/commit/a058415785d02f408e7ad1012b600c39980a3024))


### Bug Fixes

* Hide top_p from custom model config INTRC-207 ([34c5c9e](https://github.com/inooLabs/intric-frontend/commit/34c5c9ef70907aa9696fcc2774e696db11781b1a))

## [0.24.0](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.23.2...intric/web@v0.24.0) (2024-06-27)


### Features

* added model temperature and top P config (INTRC-155) ([#20](https://github.com/inooLabs/intric-frontend/issues/20)) ([6df1a5f](https://github.com/inooLabs/intric-frontend/commit/6df1a5fd8067e925c696d1587a44832db743e088))
* allow uploading of files via drag and drop in chats (INTRC-187) ([#24](https://github.com/inooLabs/intric-frontend/issues/24)) ([51620c9](https://github.com/inooLabs/intric-frontend/commit/51620c9be71e6eb53603d53ef8e8b6c92ff1a175))


### Bug Fixes

* fixed overflow-x on chats and other small bugs ([04ea84d](https://github.com/inooLabs/intric-frontend/commit/04ea84de66d10319d39e59854ed813140a3fbf0f))

## [0.23.2](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.23.1...intric/web@v0.23.2) (2024-06-25)


### Bug Fixes

* fixed a bug where a normal user could not create a collection ([c3284bf](https://github.com/inooLabs/intric-frontend/commit/c3284bffd63806dfe6ee51e921187b4baffb0bf8))

## [0.23.1](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.23.0...intric/web@v0.23.1) (2024-06-20)


### Bug Fixes

* don't show unneeded scrollbars in ChatView ([7d5f7e1](https://github.com/inooLabs/intric-frontend/commit/7d5f7e1ed29fb97a9ab470aee2b1915cd2a32bde))

## [0.23.0](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.22.1...intric/web@v0.23.0) (2024-06-20)


### Features

* add model admin page ([#18](https://github.com/inooLabs/intric-frontend/issues/18)) ([659be17](https://github.com/inooLabs/intric-frontend/commit/659be172f7f8e71b38910a0cd2222ae3116dcaf0))
* file uploads in sessions ([#16](https://github.com/inooLabs/intric-frontend/issues/16)) ([8bf04fa](https://github.com/inooLabs/intric-frontend/commit/8bf04fa236257117ecd2771b04a4be5c62875cd5))
* new and simplified collections selector ([#14](https://github.com/inooLabs/intric-frontend/issues/14)) ([3d37514](https://github.com/inooLabs/intric-frontend/commit/3d37514da27354a2481eb7859cc6d7cd7e5c6861))


### Bug Fixes

* prevent chat autoscroll when user scrolled up ([#21](https://github.com/inooLabs/intric-frontend/issues/21)) ([e06b302](https://github.com/inooLabs/intric-frontend/commit/e06b3020b4dc45597d555aaec27c8073447ba4e4))
* remove uploads form queue when they fail ([bab3bd5](https://github.com/inooLabs/intric-frontend/commit/bab3bd52a6efa944c0b3d4c3a1964cc66bb61078))
* update SelectCompletionModel to new models API (INTRC-134) ([93c13ec](https://github.com/inooLabs/intric-frontend/commit/93c13ecac5e5d63c0fc0d45e1805e8c565dabe1b))

## [0.22.1](https://github.com/inooLabs/intric-frontend/compare/intric/web@v0.22.0...intric/web@v0.22.1) (2024-06-07)


### Bug Fixes

* embedding model name in collection now visible ([#12](https://github.com/inooLabs/intric-frontend/issues/12)) ([dfd17ee](https://github.com/inooLabs/intric-frontend/commit/dfd17eebca95f77e33d94d94a7ecf9382d2ce41a))

## [0.22.0](https://github.com/inooLabs/intric-frontend/compare/intric/web-v0.21.1...intric/web@v0.22.0) (2024-06-04)


### Features

* add git info to vercel previews ([24d93d7](https://github.com/inooLabs/intric-frontend/commit/24d93d7b2875d8525a4394b69d50aa6439c6381c))
