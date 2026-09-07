---
name: harmonyos-app-dev-guide
description: "Guide for building HarmonyOS native applications from scratch. Covers project structure, configuration files (app.json5, build-profile.json5, module.json5), ArkTS coding patterns, state management, data persistence, dark mode adaptation, icon system, UX design specifications, and app store compliance checklist. Use this skill when the user mentions HarmonyOS development, ArkTS coding, Hongmeng app, 鸿蒙应用开发, building a HarmonyOS app, or needs help with HarmonyOS configuration files."
---

# HarmonyOS 应用开发指导文档

> 基于「星愿池」项目目录结构总结，适用于从零开始搭建一个新的 HarmonyOS 原生应用。

---

## 一、项目结构总览

```
MyApp/
├── AppScope/                          # 应用级配置（全局共享）
│   ├── app.json5                      # 应用身份：bundleName、版本、图标
│   └── resources/base/                # 应用级资源（图标、字符串）
├── entry/                             # 主模块（HAP）
│   ├── build-profile.json5            # 模块构建配置
│   ├── hvigorfile.ts                  # 模块构建脚本
│   ├── oh-package.json5               # 模块包描述
│   ├── obfuscation-rules.txt          # 混淆规则
│   └── src/
│       ├── main/
│       │   ├── ets/                   # ★ 全部 ArkTS 源码
│       │   ├── module.json5           # 模块清单（能力、权限、路由）
│       │   └── resources/             # 模块资源（颜色、字符串、图片、路由）
│       ├── mock/                      # 测试 mock 配置
│       └── ohosTest/                  # 单元测试
├── build-profile.json5                # 根构建配置（签名、产品、SDK 版本）
├── hvigorfile.ts                      # 根构建脚本
├── oh-package.json5                   # 根包描述（依赖管理）
├── oh-package-lock.json5              # 依赖锁文件
├── hvigor/                            # 构建系统配置
│   └── hvigor-config.json5
├── oh_modules/                        # 已安装依赖（类似 node_modules）
├── scripts/                           # 构建/部署脚本
└── CHANGELOG.md                       # 变更日志
```

### 关键原则

| 原则 | 说明 |
|---|---|
| **单模块架构** | 一个 `entry` HAP 模块承载所有业务逻辑，适合中小型应用 |
| **目录职责清晰** | `pages/` 页面、`components/` 组件、`services/` 服务、`common/` 公共定义 |
| **路由集中管理** | `main_pages.json` 只注册一个入口页面，内部通过状态管理切换子页面 |

---

## 二、配置文件详解

### 2.1 `AppScope/app.json5` — 应用身份

```json5
{
  "app": {
    "bundleName": "com.example.myapp",     // 应用唯一标识（反向域名）
    "vendor": "MyCompany",
    "versionCode": 1000000,                 // 数字版本号（递增）
    "versionName": "1.0.0",                // 显示版本
    "icon": "$media:layered_image",         // 自适应图标
    "label": "$string:app_name"            // 应用名称（引用字符串资源）
  }
}
```

### 2.2 `build-profile.json5`（根）— 构建与签名

```json5
{
  "app": {
    "signingConfigs": [
      {
        "name": "default",
        "type": "HarmonyOS",
        "material": {
          "certpath": "/path/to/certificate.cer",
          "storeFile": "/path/to/xxx.p12",
          "profile": "/path/to/xxx.p7b"
        }
      }
    ],
    "products": [
      {
        "name": "default",
        "signingConfig": "default",
        "compatibleSdkVersion": "5.0.0(12)",
        "targetSdkVersion": "5.0.0(12)",
        "runtimeOS": "HarmonyOS"
      }
    ]
  },
  "modules": [
    { "name": "entry", "srcPath": "./entry", "targets": [{ "name": "default" }] }
  ]
}
```

> **签名配置**：开发阶段使用调试证书，发布时替换为发布证书。证书在 DevEco Studio → File → Project Structure → Signing Configs 中管理。

### 2.3 `entry/src/main/module.json5` — 模块清单

```json5
{
  "module": {
    "name": "entry",
    "type": "entry",                       // entry | feature
    "mainElement": "EntryAbility",         // 入口能力
    "deviceTypes": ["phone", "tablet"],    // 支持设备
    "pages": "$profile:main_pages",        // 路由配置引用
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ets",
        "launchMode": "singleton",
        "backgroundModes": ["audioPlayback"],  // 后台能力声明
        "skills": [{ "entities": ["entity.system.home"], "actions": ["action.system.home"] }]
      }
    ],
    "requestPermissions": [
      { "name": "ohos.permission.INTERNET" },
      { "name": "ohos.permission.GET_NETWORK_INFO" }
    ]
  }
}
```

### 2.4 `resources/base/profile/main_pages.json` — 路由注册

```json
{
  "src": ["pages/MainPage"]
}
```

> **只注册一个入口页面**，所有子页面通过组件化方式在 MainPage 内切换，避免多页面栈管理的复杂性。

---

## 三、源码目录组织（`entry/src/main/ets/`）

```
ets/
├── common/                # 公共定义层
│   ├── types.ets          # 所有接口、枚举、类型定义
│   └── constants.ets      # 常量：存储键、默认数据、模板、徽章
├── entryability/          # 入口能力层
│   └── EntryAbility.ets   # UIAbility 生命周期管理
├── pages/                 # 页面层
│   ├── MainPage.ets       # 主页面（状态中心 + 子页面路由）
│   ├── RatingPage.ets     # 评分页
│   ├── GoalsPage.ets      # 目标管理页
│   ├── WishPoolPage.ets   # 心愿池页
│   └── ProfilePage.ets    # 个人中心页
├── components/            # 组件层
│   ├── TabBar.ets         # 底部导航栏
│   ├── DateSelector.ets   # 日期选择器
│   ├── StarRating.ets     # 星星评分输入
│   ├── GoalCard.ets       # 目标卡片
│   ├── RewardCard.ets     # 奖励卡片
│   ├── AddGoalModal.ets   # 添加目标弹窗
│   └── ...                # 其他可复用 UI 组件
└── services/              # 服务层
    ├── DataStore.ets      # 数据持久化（Preferences）
    ├── FileService.ets    # 文件导入导出
    ├── BadgeService.ets   # 徽章系统
    └── ...                # 其他业务服务
```

### 分层职责

```
┌─────────────────────────────────────────┐
│  pages/         页面层                   │  负责页面布局、用户交互、状态管理
├─────────────────────────────────────────┤
│  components/    组件层                   │  可复用 UI 单元，通过 props + 回调通信
├─────────────────────────────────────────┤
│  services/      服务层                   │  业务逻辑、数据操作、外部 API 调用
├─────────────────────────────────────────┤
│  common/        公共层                   │  类型定义、常量、工具函数
└─────────────────────────────────────────┘
```

---

## 四、核心编码模式

### 4.1 入口能力（EntryAbility）

```typescript
// entryability/EntryAbility.ets
import { UIAbility, AbilityConstant, Want } from '@kit.AbilityKit';
import { window } from '@kit.ArkUI';

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    // 初始化全局数据、加载持久化数据
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/MainPage', (err) => {
      if (err.code) { return; }
      // 加载主页面
    });
  }

  onWindowStageDestroy(): void { /* 释放资源 */ }
  onForeground(): void { /* 进入前台 */ }
  onBackground(): void { /* 进入后台 */ }
}
```

### 4.2 页面状态管理（单中心模式）

所有应用状态集中在 MainPage，通过 props 传递给子页面：

```typescript
// pages/MainPage.ets
@Entry
@Component
struct MainPage {
  @State currentTab: TabType = TabType.RATING;
  @State users: User[] = [];
  @State currentUser: User = INITIAL_USER;
  @State goals: Goal[] = [];
  @State records: DailyRecord[] = [];
  @State rewards: Reward[] = [];
  // ... 更多状态

  build() {
    Column() {
      // 条件渲染子页面
      if (this.currentTab === TabType.RATING) {
        RatingPage({
          goals: this.goals,
          records: this.records,
          onRate: (goal, stars) => { this.handleRate(goal, stars); }
        })
      } else if (this.currentTab === TabType.GOALS) {
        GoalsPage({ goals: this.goals, onAdd: (g) => this.addGoal(g) })
      }
      // ...

      // 底部导航
      TabBar({ currentTab: this.currentTab, onChange: (t) => this.currentTab = t })
    }
  }
}
```

### 4.3 组件通信模式（Props + Callbacks）

子组件通过构造参数接收数据，通过回调函数通知父组件：

```typescript
// components/GoalCard.ets
@Component
struct GoalCard {
  goal: Goal = {} as Goal;
  onToggle: (goal: Goal) => void = () => {};    // 回调
  onDelete: (goalId: string) => void = () => {};

  build() {
    Row() {
      Text(this.goal.title)
      Button('完成').onClick(() => this.onToggle(this.goal))
    }
  }
}
```

### 4.4 服务层单例模式

服务类在模块级别实例化为单例，提供 async 方法：

```typescript
// services/DataStore.ets
import { preferences } from '@kit.ArkData';

class DataStore {
  private store: preferences.Preferences | null = null;

  async init(context: Context): Promise<void> {
    this.store = await preferences.getPreferences(context, STORAGE_KEY);
  }

  async getData(): Promise<AppData> {
    const str = await this.store?.get(STORAGE_KEY, '{}') as string;
    return JSON.parse(str) as AppData;
  }

  async saveData(data: AppData): Promise<void> {
    await this.store?.put(STORAGE_KEY, JSON.stringify(data));
    await this.store?.flush();
  }
}

export const dataStore = new DataStore();  // 模块级单例
```

### 4.5 类型定义集中管理

所有接口、枚举在 `common/types.ets` 中统一定义：

```typescript
// common/types.ets
export interface User {
  id: string;
  name: string;
  totalStars: number;
  avatar: string;        // emoji 或 local:// 路径
}

export interface Goal {
  id: string;
  title: string;
  category: string;
  icon: string;
  maxStars: number;
  color: string;
  reminder?: GoalReminder;
}

export enum TabType {
  RATING, GOALS, WISH_POOL, PROFILE
}
```

---

## 五、资源管理

### 5.1 资源目录结构

```
resources/base/
├── element/
│   ├── color.json       # 颜色定义（支持 dark/ 覆盖）
│   ├── float.json       # 尺寸/数值定义
│   └── string.json      # 字符串资源
├── media/
│   ├── app_icon.png     # 应用图标
│   └── startIcon.png    # 启动图标
└── profile/
    └── main_pages.json  # 路由配置
```

### 5.2 暗色模式支持

```
resources/
├── base/element/color.json    # 亮色主题颜色
└── dark/element/color.json    # 暗色主题覆盖
```

系统自动根据用户主题选择对应资源文件。

### 5.3 资源引用方式

```typescript
// 在 ArkTS 中引用资源
Text($r('app.string.app_name'))          // 字符串
Image($r('app.media.app_icon'))          // 图片
.backgroundColor($r('app.color.primary')) // 颜色
```

---

## 六、数据持久化方案

### 6.1 Preferences（轻量键值存储）

适合中小型数据量（< 2KB 单条，总量建议 < 几 MB）：

```typescript
import { preferences } from '@kit.ArkData';

// 初始化
const store = await preferences.getPreferences(context, 'my_data_key');

// 写入
await store.put('user_name', '小明');
await store.flush();  // 必须 flush 才持久化

// 读取
const name = await store.get('user_name', '') as string;

// 复杂对象用 JSON 序列化
await store.put('app_data', JSON.stringify(appData));
```

### 6.2 数据结构设计建议

```typescript
// 根数据容器，版本化管理
export interface AppData {
  version: string;           // 数据版本号，用于迁移
  users: User[];
  goals: Goal[];
  records: DailyRecord[];
  rewards: Reward[];
  // ... 业务数据
}
```

> **版本迁移**：当数据结构变更时，通过 `version` 字段判断并执行增量迁移。

---

## 七、构建与运行

### 7.1 环境要求

| 工具 | 版本 |
|---|---|
| DevEco Studio | 4.0+ |
| HarmonyOS SDK | API 12+ |
| Node.js | 16+（DevEco 内置） |

### 7.2 构建命令

```bash
# 通过 Hvigor 构建（DevEco 自动调用）
hvigor assembleHap                    # 构建 HAP 包

# 签名后的 HAP 位于
entry/build/outputs/default/entry-default-signed.hap
```

### 7.3 安装到设备

```bash
# 方式一：DevEco Studio 直接运行（推荐）
# Run → Run 'entry' 或点击工具栏 ▶ 按钮

# 方式二：hdc 命令行安装
hdc install entry/build/outputs/default/entry-default-signed.hap
hdc shell aa start -a EntryAbility -b com.example.myapp
```

### 7.4 代码检查

项目已配置 `code-linter.json5`，在 DevEco Studio 中通过 **Build → Code Lint** 执行：

- `@performance/recommended` — 性能规则
- `@typescript-eslint/recommended` — TypeScript 规则
- 安全规则（AES、hash、RSA 等）

---

## 八、新项目快速上手清单

### Step 1：创建项目

在 DevEco Studio 中 **File → New → Create HarmonyOS Project**，选择 Empty Ability 模板。

### Step 2：建立目录结构

```
entry/src/main/ets/
├── common/
│   ├── types.ets          # 先定义核心数据模型
│   └── constants.ets      # 默认值、配置常量
├── entryability/
│   └── EntryAbility.ets   # 模板自动生成
├── pages/
│   └── MainPage.ets       # 主页面（状态中心）
├── components/            # 按需创建可复用组件
└── services/              # 按需创建业务服务
```

### Step 3：定义数据模型（`common/types.ets`）

先规划好核心数据结构，所有页面和服务都依赖它。

### Step 4：实现数据持久化（`services/DataStore.ets`）

创建 Preferences 单例，提供 `init()` / `getData()` / `saveData()` 方法。

### Step 5：搭建主页面框架（`pages/MainPage.ets`）

- 声明所有全局 `@State` 状态
- 实现 TabBar 切换逻辑
- 条件渲染各子页面

### Step 6：逐页面开发

每个子页面：
1. 在 `pages/` 创建页面文件
2. 定义 props 接口（从 MainPage 接收的数据和回调）
3. 提取可复用 UI 到 `components/`
4. 业务逻辑下沉到 `services/`

### Step 7：配置路由

编辑 `resources/base/profile/main_pages.json`，注册入口页面。

---

## 九、注意事项与最佳实践

| 类别 | 建议 |
|---|---|
| **状态管理** | 中小型应用用 `@State` + props 传递足够；大型应用考虑 `@Observed` / `AppStorage` |
| **组件粒度** | 单个组件不超过 300 行，超过则拆分子组件 |
| **服务层** | 所有 I/O 操作（网络、文件、数据库）放在 services/ 中，页面不直接调用系统 API |
| **类型安全** | 所有数据结构在 `types.ets` 中定义，避免使用 `any` |
| **图标资源** | HarmonyOS SVG 支持有限，简单图标用 emoji，复杂图标用 PNG |
| **图片存储** | 应用内图片存放在 `filesDir/images/`，使用 `local://` 前缀引用 |
| **权限声明** | 在 `module.json5` 的 `requestPermissions` 中声明，并在代码中动态申请运行时权限 |
| **版本管理** | 每次发版更新 `app.json5` 的 `versionCode` 和 `versionName`，同步更新 `CHANGELOG.md` |
| **代码混淆** | 正式发布前在 `build-profile.json5` 中启用 `obfuscation` |
| **备份恢复** | 声明 `backup_config.json` 启用系统备份能力 |

---

## 十、项目文件参考速查

| 文件 | 路径 | 用途 |
|---|---|---|
| 应用配置 | `AppScope/app.json5` | bundleName、版本、图标 |
| 构建签名 | `build-profile.json5` | 签名证书、SDK 版本、产品配置 |
| 模块清单 | `entry/src/main/module.json5` | 能力注册、权限声明、设备类型 |
| 路由配置 | `entry/src/main/resources/base/profile/main_pages.json` | 页面路由注册 |
| 入口能力 | `entry/src/main/ets/entryability/EntryAbility.ets` | 应用生命周期 |
| 主页面 | `entry/src/main/ets/pages/MainPage.ets` | 状态中心 + 子页面路由 |
| 类型定义 | `entry/src/main/ets/common/types.ets` | 所有接口、枚举 |
| 常量定义 | `entry/src/main/ets/common/constants.ets` | 默认数据、配置 |
| 构建脚本 | `hvigor/hvigor-config.json5` | Hvigor 构建系统配置 |
| 代码检查 | `code-linter.json5` | Lint 规则配置 |

---

## 十一、配置文件模板（通用固定 vs 项目定制）

> 每个配置文件中标注 **🔒 通用固定** 的字段直接复制，不要改动；标注 **✏️ 需定制** 的字段根据新项目实际情况修改。这样可以最大程度避免配置出错。

---

### 11.1 `AppScope/app.json5` — 应用身份

```json5
{
  "app": {
    // ✏️ 需定制：以下 3 项必须根据新项目修改
    "bundleName": "com.yourcompany.yourapp",   // 反向域名，全网唯一，发布后不可改
    "versionCode": 1000000,                     // 数字版本号，每次发版递增
    "versionName": "1.0.0",                    // 显示版本号

    // 🔒 通用固定：以下 3 项结构不变，仅替换资源文件即可
    "vendor": "example",
    "icon": "$media:layered_image",            // 引用分层图标配置，资源文件换了图标自然变
    "label": "$string:app_name"                // 引用字符串资源，改 string.json 中 app_name 即可
  }
}
```

**配套资源文件（替换内容，结构不变）：**

```
AppScope/resources/base/
├── element/string.json       // ✏️ 改 app_name 的 value 为新应用名
└── media/
    ├── layered_image.json    // 🔒 不改（引用 background + foreground）
    ├── media.json            // 🔒 不改（资源别名映射）
    ├── background.png        // ✏️ 替换为新应用的背景图（1024×1024 RGBA）
    ├── foreground.png        // ✏️ 替换为新应用的前景图（2048×1875 RGB）
    └── app_icon.png          // ✏️ 替换为新应用的整图标（2048×1875 RGB）
```

---

### 11.2 `build-profile.json5`（根级）— 构建总控

```json5
{
  "app": {
    // ✏️ 需定制：签名配置（每个开发者/团队不同）
    "signingConfigs": [
      {
        "name": "default",
        "type": "HarmonyOS",
        "material": {
          // 🔒 通用固定：字段结构不变
          "signAlg": "SHA256withECDSA",

          // ✏️ 需定制：证书文件路径和密码（从 DevEco Studio 或 AGC 获取）
          "storePassword": "你的密钥库密码",
          "keyAlias": "你的密钥别名",
          "keyPassword": "你的密钥密码",
          "storeFile": "/path/to/your.p12",
          "profile": "/path/to/your.p7b",
          "certpath": "/path/to/your.cer"
        }
      }
    ],

    "products": [
      {
        // 🔒 通用固定：以下结构和字段不变
        "name": "default",
        "signingConfig": "default",
        "runtimeOS": "HarmonyOS",
        "buildOption": {
          "strictMode": {
            "caseSensitiveCheck": true,
            "useNormalizedOHMUrl": true
          }
        },

        // ✏️ 需定制：SDK 版本（根据目标设备和 DevEco 版本调整）
        "targetSdkVersion": "6.0.1(21)",
        "compatibleSdkVersion": "6.0.0(20)"
      }
    ],

    // 🔒 通用固定：构建模式定义，原样保留
    "buildModeSet": [
      { "name": "debug" },
      { "name": "release" }
    ]
  },

  // ✏️ 需定制：模块名改为新项目的模块目录名（通常保持 "entry"）
  "modules": [
    {
      "name": "entry",
      "srcPath": "./entry",
      "targets": [
        {
          "name": "default",
          "applyToProducts": ["default"]
        }
      ]
    }
  ]
}
```

**总结：只需改签名证书路径和 SDK 版本，其余原样复制。**

---

### 11.3 `entry/build-profile.json5` — 模块级构建

```json5
{
  // 🔒 通用固定：全部原样复制，不要改动
  "apiType": "stageMode",
  "buildOption": {
    "resOptions": {
      "copyCodeResource": {
        "enable": false
      }
    }
  },
  "buildOptionSet": [
    {
      "name": "release",
      "arkOptions": {
        "obfuscation": {
          "ruleOptions": {
            "enable": false,
            "files": ["./obfuscation-rules.txt"]
          }
        }
      }
    }
  ],
  "targets": [
    { "name": "default" },
    { "name": "ohosTest" }
  ]
}
```

**此文件全部为通用固定配置，直接复制。**

---

### 11.4 `entry/src/main/module.json5` — 模块清单

```json5
{
  "module": {
    // 🔒 通用固定：以下字段结构不变
    "name": "entry",
    "type": "entry",
    "mainElement": "EntryAbility",
    "pages": "$profile:main_pages",
    "deliveryWithInstall": true,
    "installationFree": false,

    // ✏️ 需定制：设备类型（根据目标设备调整）
    "deviceTypes": ["phone", "tablet"],

    // ✏️ 需定制：描述文字
    "description": "$string:module_desc",

    "abilities": [
      {
        // 🔒 通用固定：能力注册结构
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ets",
        "exported": true,

        // 🔒 通用固定：启动画面配置（替换图标资源文件即可，引用不变）
        "startWindowIcon": "$media:startIcon",
        "startWindowBackground": "$color:start_window_background",

        // ✏️ 需定制：描述文字
        "description": "$string:EntryAbility_desc",

        // ✏️ 需定制：后台模式（按需声明，不需要就留空数组 []）
        "backgroundModes": ["audioPlayback"],

        // 🔒 通用固定：桌面启动器入口配置，原样保留
        "skills": [
          {
            "entities": ["entity.system.home"],
            "actions": ["action.system.home"]
          }
        ]
      }
    ],

    // ✏️ 需定制：权限列表（按需增删，不需要的权限整条删除）
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET",
        "reason": "$string:permission_internet_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      },
      {
        "name": "ohos.permission.GET_NETWORK_INFO",
        "reason": "$string:permission_network_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
      },
      {
        "name": "ohos.permission.KEEP_BACKGROUND_RUNNING",
        "reason": "$string:permission_background_reason",
        "usedScene": { "abilities": ["EntryAbility"], "when": "always" }
      }
    ]
  }
}
```

**配套资源文件（替换内容，结构不变）：**

```
entry/src/main/resources/
├── base/
│   ├── element/
│   │   ├── color.json        // 🔒 结构不变，按需改颜色值
│   │   ├── string.json       // ✏️ 改描述文字（module_desc、EntryAbility_desc、permission_*_reason 等）
│   │   └── float.json        // 🔒 按需调整
│   ├── media/
│   │   ├── media.json        // 🔒 不改（资源别名映射）
│   │   ├── start_icon.png    // ✏️ 替换启动图标（1280×1280）
│   │   └── app_icon.png      // ✏️ 替换应用图标（2048×1875）
│   └── profile/
│       └── main_pages.json   // 🔒 结构不变（见下节）
└── dark/
    └── element/
        └── color.json        // 🔒 结构不变，按需改暗色颜色值
```

---

### 11.5 `resources/base/profile/main_pages.json` — 路由注册

```json
{
  // 🔒 通用固定：结构不变
  // ✏️ 需定制：src 数组中的页面路径改为新项目的页面
  "src": ["pages/MainPage"]
}
```

**单页面模式下只需改一个页面名。多页面模式按需添加：**
```json
{ "src": ["pages/MainPage", "pages/DetailPage"] }
```

---

### 11.6 `oh-package.json5`（根级）— 项目包描述

```json5
{
  // 🔒 通用固定：以下结构原样复制
  "modelVersion": "6.0.1",
  "description": "Please describe the basic information.",

  // ✏️ 需定制：运行时依赖（没有就留空对象 {}）
  "dependencies": {},

  // 🔒 通用固定：开发依赖，原样保留
  "devDependencies": {
    "@ohos/hypium": "1.0.24",
    "@ohos/hamock": "1.0.0"
  }
}
```

---

### 11.7 `entry/oh-package.json5` — 模块包描述

```json5
{
  // ✏️ 需定制：模块名
  "name": "entry",

  // 🔒 通用固定：以下字段原样复制
  "version": "1.0.0",
  "description": "Please describe the basic information.",
  "main": "",
  "author": "",
  "license": "",
  "dependencies": {}
}
```

---

### 11.8 配置速查表：哪些能动哪些不能动

| 文件 | 🔒 通用固定（原样复制） | ✏️ 需定制（必须改） |
|---|---|---|
| **app.json5** | `icon`、`label` 引用格式 | `bundleName`、`versionCode`、`versionName` |
| **build-profile.json5（根）** | `signingConfigs` 结构、`products` 结构、`buildModeSet`、`modules` 结构 | 签名证书路径/密码、SDK 版本号 |
| **entry/build-profile.json5** | **全部** | 无 |
| **module.json5** | `type`、`mainElement`、`pages`、`deliveryWithInstall`、`installationFree`、`srcEntry`、`startWindow*`、`skills` | `deviceTypes`、`description`、`backgroundModes`、`requestPermissions` 列表 |
| **main_pages.json** | JSON 结构 | `src` 中的页面路径 |
| **oh-package.json5（根）** | `modelVersion`、`devDependencies` | `dependencies` |
| **entry/oh-package.json5** | `version`、`main`、`author`、`license`、`dependencies` | `name` |

> **安全原则**：不确定的字段就保持原值。所有 `$media:`、`$string:`、`$color:`、`$profile:` 引用格式不要改，只替换它们指向的资源文件内容。

### 11.1 `AppScope/app.json5` — 应用级配置

这是整个应用的「身份证」，定义应用的全局属性，所有模块共享。

```json5
{
  "app": {
    "bundleName": "com.bigchange.starcollection",
    "vendor": "example",
    "versionCode": 1005000,
    "versionName": "1.5.0",
    "icon": "$media:layered_image",
    "label": "$string:app_name"
  }
}
```

| 字段 | 类型 | 必填 | 含义 |
|---|---|---|---|
| `bundleName` | string | ✅ | **应用唯一标识**。采用反向域名格式（如 `com.company.appname`），全网唯一。用于应用商店索引、数据隔离、权限沙箱。一旦发布后**不可修改**，否则系统视为全新应用。 |
| `vendor` | string | ✅ | **开发商/作者名称**。纯信息字段，显示在应用商店详情中，不影响运行行为。 |
| `versionCode` | number | ✅ | **内部版本号**。纯数字，每次发版**必须递增**。系统和应用商店用它判断版本新旧、是否需要升级。格式建议：主版本×1000000 + 次版本×1000 + 修订号，如 `1.5.0` → `1005000`。 |
| `versionName` | string | ✅ | **显示版本号**。用户可见的版本字符串（如 `"1.5.0"`），展示在应用商店和设置中。仅做展示，不参与版本比较逻辑。 |
| `icon` | string | ✅ | **应用图标资源引用**。格式为 `$media:{资源名}`，指向 `resources/base/media/` 下的资源。使用 `layered_image` 时引用分层图标配置，系统自动合成背景+前景。 |
| `label` | string | ✅ | **应用名称资源引用**。格式为 `$string:{字符串名}`，指向 `resources/base/element/string.json` 中的条目。此处引用 `app_name` → `"星愿池"`，显示在桌面图标下方和系统设置中。 |

> **关键约束**：`bundleName` 和 `versionCode` 一旦上架后修改，会导致应用无法覆盖安装（系统视为不同应用）。发版时只需递增 `versionCode` 和更新 `versionName`。

---

### 11.2 `build-profile.json5`（根级）— 构建、签名与产品配置

这是 Hvigor 构建系统的总配置，定义签名方案、产品变体、构建模式和模块列表。

```json5
{
  "app": {
    "signingConfigs": [ /* ... */ ],
    "products": [ /* ... */ ],
    "buildModeSet": [ /* ... */ ]
  },
  "modules": [ /* ... */ ]
}
```

#### 11.2.1 `app.signingConfigs[]` — 签名配置

```json5
{
  "name": "default",                    // 配置名称，被 products 引用
  "type": "HarmonyOS",                  // 签名类型：HarmonyOS（鸿蒙）| OpenHarmony（开源鸿蒙）
  "material": {
    "storePassword": "000000...",       // 密钥库密码（加密存储，非明文）
    "keyAlias": "stars_collection",     // 密钥别名
    "keyPassword": "000000...",         // 密钥密码（加密存储）
    "signAlg": "SHA256withECDSA",       // 签名算法（ECDSA 比 RSA 更安全高效）
    "storeFile": "/path/to/xxx.p12",    // 密钥库文件路径（.p12 格式）
    "profile": "/path/to/xxx.p7b",      // 签名配置文件（.p7b，含设备指纹和权限声明）
    "certpath": "/path/to/xxx.cer"      // 数字证书路径（.cer，含公钥和身份信息）
  }
}
```

| 字段 | 含义 |
|---|---|
| `name` | 配置的引用名，在 `products[].signingConfig` 中使用 |
| `type` | `HarmonyOS` 用于华为应用市场分发；`OpenHarmony` 用于开源鸿蒙设备 |
| `material.storeFile` | PKCS#12 格式的密钥库，包含签名私钥。由 DevEco Studio 自动生成或从 AGC 下载 |
| `material.profile` | 签名配置文件（Provision Profile），包含应用权限白名单、可安装设备列表。调试版绑定开发者设备 UDID，发布版不限设备 |
| `material.certpath` | X.509 数字证书，包含公钥和开发者身份信息。调试证书和发布证书不同 |
| `material.storePassword` | 密钥库的密码，DevEco 加密存储。手动配置时需填写明文 |
| `material.keyAlias` | 密钥库中的密钥条目名称 |
| `material.keyPassword` | 该密钥条目的密码 |
| `material.signAlg` | 签名算法。`SHA256withECDSA` 是当前推荐算法 |

> **调试 vs 发布**：调试证书（debug）绑定开发者设备 UDID，只能在该设备安装；发布证书（release）不限设备，用于应用商店上架。星愿池项目通过注释切换两种证书路径。

#### 11.2.2 `app.products[]` — 产品变体

```json5
{
  "name": "default",                            // 产品名称
  "signingConfig": "default",                   // 引用哪个签名配置
  "targetSdkVersion": "6.0.1(21)",              // 目标 SDK 版本
  "compatibleSdkVersion": "6.0.0(20)",          // 最低兼容 SDK 版本
  "runtimeOS": "HarmonyOS",                     // 运行时系统
  "buildOption": {
    "strictMode": {
      "caseSensitiveCheck": true,               // 大小写敏感检查
      "useNormalizedOHMUrl": true               // 使用标准化 OHM URL
    }
  }
}
```

| 字段 | 含义 |
|---|---|
| `name` | 产品变体名。可以定义多个产品（如 `free`/`pro`），对应不同的签名和 SDK 配置 |
| `signingConfig` | 引用 `signingConfigs[]` 中的 `name`，决定该产品用哪套签名 |
| `targetSdkVersion` | **目标 SDK 版本**。格式为 `"主版本.次版本.修订号(API级别)"`。应用基于此版本 API 开发，系统会启用该版本对应的行为和限制。`6.0.1(21)` = API 21 |
| `compatibleSdkVersion` | **最低兼容版本**。低于此版本的设备无法安装。格式同上。`6.0.0(20)` = API 20，即 API 20 以下设备不兼容 |
| `runtimeOS` | 运行系统。`HarmonyOS` = 华为鸿蒙（有 HMS）；`OpenHarmony` = 开源鸿蒙 |
| `buildOption.strictMode.caseSensitiveCheck` | 启用文件路径大小写检查，避免 Linux/Windows 大小写不一致导致的运行时错误 |
| `buildOption.strictMode.useNormalizedOHMUrl` | 使用标准化的 OHM（OpenHarmony Module）URL 格式，确保模块引用路径规范 |

> **版本号关系**：`targetSdkVersion` ≥ `compatibleSdkVersion`。差距越大，向下兼容范围越广，但无法使用新 API 特性。

#### 11.2.3 `app.buildModeSet[]` — 构建模式

```json5
[
  { "name": "debug" },      // 调试模式：不混淆、含调试符号、可断点调试
  { "name": "release" }     // 发布模式：可启用混淆、优化、签名
]
```

| 模式 | 特点 |
|---|---|
| `debug` | 默认模式。包含调试信息，不混淆代码，支持 DevEco 断点调试、日志输出 |
| `release` | 发布模式。可在模块级 `build-profile.json5` 中配置混淆规则，移除调试日志 |

在 DevEco Studio 中通过 **Build → Build Mode** 切换，或在构建命令中指定。

#### 11.2.4 `modules[]` — 模块列表

```json5
[
  {
    "name": "entry",                    // 模块名，与目录名一致
    "srcPath": "./entry",              // 模块源码相对路径
    "targets": [
      {
        "name": "default",             // 构建目标名
        "applyToProducts": ["default"] // 该目标应用到哪些产品变体
      }
    ]
  }
]
```

| 字段 | 含义 |
|---|---|
| `name` | 模块名称，必须与模块目录名和 `module.json5` 中的 `module.name` 一致 |
| `srcPath` | 模块源码目录的相对路径（相对于项目根目录） |
| `targets[].name` | 构建目标名称。`default` 是主目标，`ohosTest` 是测试目标 |
| `targets[].applyToProducts` | 该构建目标应用到哪些产品变体。`["default"]` 表示只在 default 产品下构建此目标 |

> **多模块场景**：大型应用可拆分为 `entry`（主模块）+ 多个 `feature` 模块（如 `pay_module`、`share_module`），实现按需加载。星愿池是单模块架构。

---

### 11.3 `entry/src/main/module.json5` — 模块清单

这是模块的「注册表」，定义模块的能力、权限、路由和设备兼容性。

```json5
{
  "module": {
    "name": "entry",
    "type": "entry",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": ["phone", "tablet"],
    "deliveryWithInstall": true,
    "installationFree": false,
    "pages": "$profile:main_pages",
    "abilities": [ /* ... */ ],
    "requestPermissions": [ /* ... */ ]
  }
}
```

#### 11.3.1 模块基本信息

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | string | 模块名称，与目录名和 `build-profile.json5` 中的模块名一致 |
| `type` | string | 模块类型。`entry` = 主模块（应用入口，必须有且只有一个）；`feature` = 功能模块（可选，按需加载） |
| `description` | string | 模块描述。`$string:module_desc` 引用字符串资源 → `"星愿池主模块"` |
| `mainElement` | string | **入口能力名称**。指向 `abilities[]` 中的某个 `name`，系统启动应用时首先加载此能力。必须与 `abilities[]` 中某个条目的 `name` 完全匹配 |
| `deviceTypes` | string[] | **支持的设备类型（必填，不能为空）**。详见下方 11.3.1a 设备类型规范 |
| `deliveryWithInstall` | boolean | **随安装分发**。`true` = 应用安装时一起下载此模块；`false` = 按需下载（用于大型可选模块） |
| `installationFree` | boolean | **免安装应用**。`true` = 免安装（类似小程序，通过链接直接打开）；`false` = 需要安装。免安装应用有大小和权限限制 |
| `pages` | string | **路由配置引用**。`$profile:main_pages` 指向 `resources/base/profile/main_pages.json` 文件 |

#### 11.3.1a `deviceTypes` 设备类型规范（上架必检）

每个 HAP 包的 `module.json5` 中 `deviceTypes` 字段**必须明确声明支持的设备类型**，这是应用上架的硬性要求。

**合法值：**

| 值 | 设备 | 说明 |
|---|---|---|
| `phone` | 手机 | 最常用的配置，绝大多数应用必选 |
| `tablet` | 平板 | 需要适配大屏布局 |
| `tv` | 智慧屏 | 需要适配遥控器交互 |
| `2in1` | 二合一设备 | 平板/笔记本形态切换 |
| `wearable` | 智能手表 | 小屏圆形/方形表盘适配 |
| `car` | 车机 | 驾驶场景交互适配 |
| `default` | 默认设备 | ⚠️ 见下方警告 |

**硬性规则：**

```json5
// ❌ 致命错误 — 为空，无法构建
"deviceTypes": []

// ❌ 错误 — default 可以编译但无法上架发布
"deviceTypes": ["default"]

// ❌ 错误 — 混入 default，上架被拒
"deviceTypes": ["phone", "default"]

// ✅ 正确 — 至少声明一个真实设备类型
"deviceTypes": ["phone"]

// ✅ 正确 — 多设备支持
"deviceTypes": ["phone", "tablet"]
```

> **⚠️ 关于 `default` 的警告**：配置为 `default` 虽然可以正常编译构建，但是**不支持发布上架**。应用市场审核会拒绝包含 `default` 的包。如果不确定支持哪些设备，使用 `phone` 代替 `default`。

**常见配置组合：**

```json5
// 手机应用（最常见）
"deviceTypes": ["phone"]

// 手机 + 平板
"deviceTypes": ["phone", "tablet"]

// 全设备（需要每个设备都做过适配测试）
"deviceTypes": ["phone", "tablet", "tv", "2in1", "wearable", "car"]
```

> **星愿池配置**：`"deviceTypes": ["phone", "tablet"]` — 支持手机和平板。

#### 11.3.2 `abilities[]` — 能力声明

```json5
{
  "name": "EntryAbility",
  "srcEntry": "./ets/entryability/EntryAbility.ets",
  "description": "$string:EntryAbility_desc",
  "startWindowIcon": "$media:startIcon",
  "startWindowBackground": "$color:start_window_background",
  "exported": true,
  "backgroundModes": ["audioPlayback"],
  "skills": [
    {
      "entities": ["entity.system.home"],
      "actions": ["action.system.home"]
    }
  ]
}
```

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | string | 能力名称，被 `mainElement` 引用。全局唯一标识 |
| `srcEntry` | string | 能力源码文件的相对路径（相对于 `ets/` 目录）。指向实现 `UIAbility` 的 `.ets` 文件 |
| `description` | string | 能力描述，引用字符串资源 |
| `startWindowIcon` | string | **启动窗口图标**。冷启动时显示在启动画面中的图标，`$media:startIcon` 引用 `media.json` 中的别名 → `start_icon.png` |
| `startWindowBackground` | string | **启动窗口背景色**。`$color:start_window_background` 引用 `color.json` → 亮色 `#FFFFFF`，暗色 `#000000`。系统自动根据主题选择 |
| `exported` | boolean | **是否可被外部调用**。`true` = 其他应用可通过 Want 启动此能力；`false` = 仅应用内部可调用。入口能力必须为 `true` |
| `backgroundModes` | string[] | **后台运行模式声明**。`audioPlayback` = 音频播放后台，`dataTransfer` = 数据传输，`location` = 定位等。声明后应用可在对应场景保持后台运行。与 `KEEP_BACKGROUND_RUNNING` 权限配合使用 |
| `skills[]` | object[] | **Intent 过滤器**。定义此能力响应哪些 Intent（意图） |
| `skills[].entities` | string[] | 能力的实体类型。`entity.system.home` = 桌面启动器入口，出现在系统桌面 |
| `skills[].actions` | string[] | 能力的 action 类型。`action.system.home` = 响应 HOME 意图，点击图标启动此能力 |

> **能力类型**：`EntryAbility` 继承自 `UIAbility`，是有界面的能力。还有 `ServiceAbility`（无界面后台服务）和 `DataAbility`（数据共享），但 HarmonyOS API 9+ 已不推荐使用后两者。

#### 11.3.3 `requestPermissions[]` — 权限声明

```json5
{
  "name": "ohos.permission.INTERNET",
  "reason": "$string:permission_internet_reason",
  "usedScene": {
    "abilities": ["EntryAbility"],
    "when": "inuse"
  }
}
```

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | string | **权限标识符**。`ohos.permission.` 前缀是系统权限命名空间 |
| `reason` | string | **申请理由**。引用字符串资源，向用户解释为什么需要此权限。仅对敏感权限（运行时权限）有效，系统会在弹窗中展示此理由 |
| `usedScene.abilities` | string[] | 使用此权限的能力列表。说明哪些能力会用到此权限 |
| `usedScene.when` | string | **使用时机**。`inuse` = 仅在应用使用期间（前台）；`always` = 始终允许（后台也需要）。`always` 需要更强的理由说明 |

**星愿池使用的权限：**

| 权限 | 级别 | reason | 用途 |
|---|---|---|---|
| `INTERNET` | 普通 | `"用于AI功能网络请求"` | 发起 HTTP 请求（AI 接口、WebDAV） |
| `GET_NETWORK_INFO` | 普通 | `"用于获取网络状态"` | 检查网络是否可用（WebDAV 同步前判断） |
| `KEEP_BACKGROUND_RUNNING` | 系统授权 | `"用于尝试保持应用后台运行"` | 配合 `backgroundModes` 保活定时提醒 |

> **权限级别**：`普通` 权限安装时自动授予；`敏感` 权限（如相机、存储）需要运行时弹窗授权；`系统授权` 权限需要系统签名或特殊申请。

---

### 11.4 `resources/base/profile/main_pages.json` — 路由注册

```json
{
  "src": [
    "pages/MainPage"
  ]
}
```

| 字段 | 类型 | 含义 |
|---|---|---|
| `src` | string[] | **页面路由表**。数组中每个元素是 `pages/` 目录下的页面文件路径（不含 `.ets` 后缀）。第一个页面为应用启动后的默认首页 |

**路由机制：**

```
系统启动应用
  → 读取 module.json5 → mainElement = "EntryAbility"
  → 加载 EntryAbility.ets → onWindowStageCreate()
    → windowStage.loadContent('pages/MainPage')
      → 系统在 main_pages.json 的 src 中查找 "pages/MainPage"
        → 找到 → 加载并渲染 MainPage.ets
        → 未找到 → 报错
```

**多页面 vs 单页面路由：**

```json
// 方案一：单页面路由（星愿池采用）
// 所有子页面在 MainPage 内通过状态切换，不注册为独立路由
{ "src": ["pages/MainPage"] }

// 方案二：多页面路由
// 每个页面独立注册，通过 router.pushUrl() 跳转
{ "src": ["pages/MainPage", "pages/DetailPage", "pages/SettingsPage"] }
```

| 方案 | 优点 | 缺点 |
|---|---|---|
| 单页面路由 | 状态共享方便、无页面栈管理、切换流畅 | MainPage 文件过大（星愿池 1900+ 行） |
| 多页面路由 | 页面解耦、单文件小、支持页面栈返回 | 状态传递复杂、页面间通信需 AppStorage 或 EventHub |

> **命名规范**：页面路径使用 PascalCase（如 `MainPage`），与组件命名一致。路由路径区分大小写（`mainpage` ≠ `MainPage`）。

---

### 11.5 补充配置文件

#### `entry/build-profile.json5` — 模块级构建配置

```json5
{
  "apiType": "stageMode",
  "buildOption": {
    "resOptions": {
      "copyCodeResource": {
        "enable": false
      }
    }
  },
  "buildOptionSet": [
    {
      "name": "release",
      "arkOptions": {
        "obfuscation": {
          "ruleOptions": {
            "enable": false,
            "files": ["./obfuscation-rules.txt"]
          }
        }
      }
    }
  ],
  "targets": [
    { "name": "default" },
    { "name": "ohosTest" }
  ]
}
```

| 字段 | 含义 |
|---|---|
| `apiType` | API 模式。`stageMode` = Stage 模型（API 9+ 推荐），`faModel` = FA 模型（已废弃）。新项目必须用 `stageMode` |
| `buildOption.resOptions.copyCodeResource.enable` | 是否将代码中的资源引用复制到产物中。`false` = 不复制，减少包体积 |
| `buildOptionSet[].name` | 构建模式名称，与根级 `buildModeSet` 对应 |
| `buildOptionSet[].arkOptions.obfuscation.ruleOptions.enable` | 是否启用代码混淆。`true` = 按规则混淆代码，增加反编译难度 |
| `buildOptionSet[].arkOptions.obfuscation.ruleOptions.files` | 混淆规则文件路径。定义哪些类名/方法名不混淆（keep 规则） |
| `targets[]` | 构建目标列表。`default` = 主构建目标，`ohosTest` = 测试构建目标 |

#### `oh-package.json5`（根级）— 项目包描述

```json5
{
  "modelVersion": "6.0.1",
  "description": "Please describe the basic information.",
  "dependencies": {},
  "devDependencies": {
    "@ohos/hypium": "1.0.24",
    "@ohos/hamock": "1.0.0"
  }
}
```

| 字段 | 含义 |
|---|---|
| `modelVersion` | 包管理模型版本，与 HarmonyOS SDK 版本对应 |
| `dependencies` | 运行时依赖。第三方库（如网络库、UI 库）在此声明 |
| `devDependencies` | 开发时依赖。`@ohos/hypium` = 单元测试框架，`@ohos/hamock` = Mock 框架。不打包到最终产物 |

#### `entry/oh-package.json5` — 模块包描述

```json5
{
  "name": "entry",
  "version": "1.0.0",
  "description": "Please describe the basic information.",
  "main": "",
  "author": "",
  "license": "",
  "dependencies": {}
}
```

| 字段 | 含义 |
|---|---|
| `name` | 模块包名，被其他模块通过 `dependencies` 引用时使用 |
| `version` | 模块版本号（语义化版本） |
| `main` | 模块入口文件。留空则使用默认入口 |
| `dependencies` | 该模块特有的依赖（合并根级依赖） |

---

### 11.6 配置文件之间的引用关系

```
AppScope/app.json5
  ├── icon → $media:layered_image
  │            └── AppScope/resources/base/media/layered_image.json
  │                  ├── background → $media:background → background.png
  │                  └── foreground → $media:foreground → foreground.png
  └── label → $string:app_name
               └── AppScope/resources/base/element/string.json → "星愿池"

build-profile.json5（根）
  ├── signingConfigs[] ←── products[].signingConfig 引用
  └── modules[].name ←── modules[].srcPath 指向模块目录

entry/src/main/module.json5
  ├── mainElement → abilities[].name（"EntryAbility"）
  ├── pages → $profile:main_pages
  │             └── resources/base/profile/main_pages.json → ["pages/MainPage"]
  ├── abilities[].srcEntry → ./ets/entryability/EntryAbility.ets
  ├── abilities[].startWindowIcon → $media:startIcon
  │                                  └── resources/base/media/media.json → start_icon.png
  ├── abilities[].startWindowBackground → $color:start_window_background
  │                                        └── resources/base/element/color.json → #FFFFFF / #000000
  ├── abilities[].description → $string:EntryAbility_desc
  │                               └── resources/base/element/string.json → "星愿池应用入口"
  └── requestPermissions[].reason → $string:permission_xxx_reason
                                      └── resources/base/element/string.json → "用于..."
```

---

## 十二、深色模式适配规范

> **鸿蒙 UX 强制要求**：应用必须正确适配深色模式。未适配的应用在审核时会被驳回。新增功能必须从第一行代码就遵循本规范。

### 12.1 鸿蒙深色模式工作原理

系统切换深色模式时，资源加载优先级如下：

```
用户选择深色模式
  → 系统优先加载 resources/dark/ 下的资源
  → dark/ 中没有对应文件 → 回退加载 resources/base/
```

**颜色资源是最关键的适配点**：`base/element/color.json` 定义亮色值，`dark/element/color.json` 定义暗色值，系统自动切换。

```
resources/
├── base/element/color.json        ← 亮色模式颜色（默认）
│   { "name": "bg_primary", "value": "#F8FAFC" }     浅灰背景
│   { "name": "text_primary", "value": "#1E293B" }   深色文字
│
└── dark/element/color.json        ← 深色模式颜色（自动覆盖）
    { "name": "bg_primary", "value": "#0F172A" }     深色背景
    { "name": "text_primary", "value": "#F1F5F9" }   浅色文字
```

**代码中通过 `$r('app.color.xxx')` 引用颜色资源，系统会自动选择对应模式的值。这是唯一正确的颜色引用方式。**

---

### 12.2 当前问题：硬编码颜色

项目中存在大量硬编码的十六进制颜色值，深色模式下无法自动切换：

```
// ❌ 错误 — 硬编码颜色，深色模式下不变
.fontColor('#1E293B')
.backgroundColor('#FFFFFF')

// ✅ 正确 — 资源引用，系统自动切换
.fontColor($r('app.color.text_primary'))
.backgroundColor($r('app.color.bg_card'))
```

**统计**：当前项目中约 223 处硬编码颜色 vs 425 处资源引用，约 34% 的颜色未适配深色模式。

---

### 12.3 新增功能的硬性规则

#### 规则一：禁止在 ArkTS 中直接写颜色值

```typescript
// ❌ 以下写法全部禁止
.fontColor('#1E293B')
.fontColor('#FF6B7280')
.backgroundColor('#FFFFFF')
.backgroundColor('rgba(0,0,0,0.5)')
.color('#FBBF24')
.borderColor('#E2E8F0')
.placeholderColor('#9CA3AF')

// ✅ 全部改为资源引用
.fontColor($r('app.color.text_primary'))
.fontColor($r('app.color.text_hint'))
.backgroundColor($r('app.color.bg_card'))
.backgroundColor($r('app.color.modal_mask'))
.color($r('app.color.star_color'))
.borderColor($r('app.color.border_color'))
.placeholderColor($r('app.color.text_hint'))
```

#### 规则二：新增颜色必须同时定义 base 和 dark

每新增一个颜色，必须在两个文件中同时添加：

```json5
// entry/src/main/resources/base/element/color.json（亮色）
{ "name": "my_new_color", "value": "#E0F2F1" }

// entry/src/main/resources/dark/element/color.json（暗色）
{ "name": "my_new_color", "value": "#0D3D38" }
```

> 如果 dark 中缺少对应条目，该颜色在深色模式下会回退到 base 的亮色值，导致亮色背景上出现亮色文字（不可见）。

#### 规则三：颜色语义化命名

颜色名应表达**用途**而非**色值**：

```json5
// ❌ 错误命名 — 说的是颜色不是用途
{ "name": "teal_500", "value": "#14B8A6" }
{ "name": "gray_100", "value": "#F1F5F9" }

// ✅ 正确命名 — 说的是用途，色值可以随时换
{ "name": "primary", "value": "#14B8A6" }
{ "name": "bg_primary", "value": "#F1F5F9" }
```

---

### 12.4 已有颜色资源速查

以下是 `color.json` 中已定义的颜色语义，新功能**优先复用**，不要重复定义：

| 颜色名 | 亮色值 | 暗色值 | 用途 |
|---|---|---|---|
| `bg_primary` | `#F8FAFC` | `#0F172A` | 页面主背景 |
| `bg_card` | `#FFFFFF` | `#1E293B` | 卡片背景 |
| `text_primary` | `#1E293B` | `#F1F5F9` | 主文字 |
| `text_secondary` | `#64748B` | `#94A3B8` | 次要文字 |
| `text_hint` | `#6B7280` | `#64748B` | 提示/占位文字 |
| `text_tertiary` | `#94A3B8` | `#64748B` | 第三级文字 |
| `border_color` | `#E2E8F0` | `#334155` | 边框/分割线 |
| `primary` / `primary_color` | `#14B8A6` | `#14B8A6` | 主题色（深浅不变） |
| `primary_light` | `#CCF7F4` | `#0D4F4A` | 主题色浅色变体 |
| `star_color` | `#FBBF24` | `#FBBF24` | 星星颜色（深浅不变） |
| `star_bg` | `#FEF3C7` | `#422006` | 星星背景 |
| `modal_mask` | `#80000000` | `#CC000000` | 弹窗遮罩 |
| `modal_bg` | `#FFFFFF` | `#1E293B` | 弹窗背景 |
| `modal_input_bg` | `#F8FAFC` | `#334155` | 弹窗输入框背景 |
| `modal_button_cancel_bg` | `#F1F5F9` | `#334155` | 取消按钮背景 |
| `modal_button_cancel_text` | `#64748B` | `#94A3B8` | 取消按钮文字 |
| `modal_button_danger_bg` | `#FEE2E2` | `#450A0A` | 危险按钮背景 |
| `modal_button_danger_text` | `#EF4444` | `#FCA5A5` | 危险按钮文字 |
| `modal_warning_bg` | `#FEF3C7` | `#422006` | 警告背景 |
| `success_color` | `#10B981` | `#10B981` | 成功色 |
| `error_color` | `#EF4444` | `#EF4444` | 错误色 |
| `warning_color` | `#F59E0B` | `#F59E0B` | 警告色 |
| `info` | `#3B82F6` | `#3B82F6` | 信息色 |

> **设计原则**：主题色、功能色（成功/错误/警告）深浅模式保持一致；背景色和文字色必须深浅反转。

---

### 12.5 特殊场景处理

#### 场景一：渐变色

渐变色不能直接用资源引用，需要在代码中处理：

```typescript
// ❌ 硬编码渐变
.linearGradient({
  direction: GradientDirection.Right,
  colors: [['#14B8A6', 0], ['#2DD4BF', 1]]
})

// ✅ 方案：渐变色也提取到 color.json，逐色引用
.linearGradient({
  direction: GradientDirection.Right,
  colors: [
    [$r('app.color.gradient_start').toString(), 0],
    [$r('app.color.gradient_end').toString(), 1]
  ]
})
```

> 如果渐变色在深色模式下不需要变化，可以保持硬编码，但必须在代码注释中标注 `// dark-mode: fixed gradient, intentional`。

#### 场景二：rgba 透明度颜色

```typescript
// ❌ 硬编码 rgba
.backgroundColor('rgba(0,0,0,0.5)')
.fontColor('rgba(255,255,255,0.9)')

// ✅ 提取到 color.json（带透明度的十六进制）
// color.json: { "name": "overlay_bg", "value": "#80000000" }
// color.json: { "name": "text_on_primary", "value": "#E6FFFFFF" }
.backgroundColor($r('app.color.overlay_bg'))
.fontColor($r('app.color.text_on_primary'))
```

> 透明度用十六进制前两位表示：`80` = 50%，`CC` = 80%，`E6` = 90%。

#### 场景三：业务颜色（如目标分类色）

业务颜色（GOAL_COLORS 等）如果在深浅模式下不需要变化，有两种处理方式：

```typescript
// 方案 A：保持硬编码，但在 dark/color.json 中无对应条目即可
// 适用于：强调色、分类色、品牌色 — 深浅模式视觉一致
export const GOAL_COLORS: Map<string, string> = new Map([
  ['劳动', '#CCF7F4'],   // 这些是分类强调色，深浅模式保持一致
  ['学习', '#DBEAFE'],
  ['健康', '#DCFCE7'],
  ['其他', '#F3E8FF']
]);

// 方案 B（推荐）：也提取到 color.json，方便全局调整
// base/color.json: { "name": "goal_labor", "value": "#CCF7F4" }
// dark/color.json: { "name": "goal_labor", "value": "#0D3D38" }  // 暗色变体
```

> **判断标准**：如果该颜色用作背景且上面有文字，必须适配深色模式；如果只是装饰性色块/边框点缀，可以保持不变。

---

### 12.6 新功能开发检查清单

每次提交新功能代码前，逐项检查：

```
□ 所有 .fontColor() 使用 $r('app.color.xxx') 资源引用
□ 所有 .backgroundColor() 使用 $r('app.color.xxx') 资源引用
□ 所有 .borderColor() / .color() 使用 $r('app.color.xxx') 资源引用
□ 所有 .placeholderColor() 使用 $r('app.color.xxx') 资源引用
□ 新增的颜色在 base/color.json 和 dark/color.json 中都有定义
□ 颜色命名是语义化的（用途而非色值）
□ 无遗留的十六进制颜色硬编码（'#XXXXXX'）
□ 无遗留的 rgba() 硬编码
□ 在深色模式下实际测试过（设置 → 显示和亮度 → 深色模式）
```

**快速自查命令：**
```bash
# 查找代码中所有硬编码颜色
grep -rn '#[0-9A-Fa-f]\{6,8\}\|rgba(' entry/src/main/ets/your-new-file.ets

# 如果有输出，说明还有未适配的颜色
```

---

## 十三、图标体系详解

HarmonyOS 应用涉及多层图标，从系统桌面到应用内业务图标，每层有不同的规范和处理方式。

### 11.1 图标分层总览

```
┌──────────────────────────────────────────────────────────┐
│  系统层图标                                               │
│  ├── 应用桌面图标（自适应图标 / Layered Image）            │
│  ├── 启动画面图标（Splash / Start Window Icon）           │
│  └── 通知/任务栏图标                                      │
├──────────────────────────────────────────────────────────┤
│  应用内图标                                               │
│  ├── Emoji 图标（目标、徽章、头像 — 用 Text 组件渲染）     │
│  ├── 本地图片图标（用户拍照/选图 — 用 Image 组件渲染）     │
│  └── Base64 / 网络图片（远程资源 — 用 Image 组件渲染）     │
└──────────────────────────────────────────────────────────┘
```

### 11.2 系统层图标 — 应用桌面图标（自适应图标）

HarmonyOS 使用 **Layered Image（分层图标）** 实现自适应图标，支持系统在不同设备上对图标进行缩放、裁剪和视觉效果处理。

#### 文件结构

```
AppScope/resources/base/media/
├── layered_image.json       # 分层图标配置（引用 background + foreground）
├── background.png           # 背景层（1024×1024, RGBA）
├── foreground.png           # 前景层（2048×1875, RGB）
├── foreground_1.png         # 备用前景（1024×1024, RGBA）
├── app_icon.png             # 传统整图标（2048×1875, RGB）— 回退用
└── media.json               # 资源别名映射
```

#### 配置关系

```json5
// AppScope/app.json5
"icon": "$media:layered_image"    // 引用分层图标

// AppScope/resources/base/media/layered_image.json
{
  "layered-image": {
    "background": "$media:background",   // 指向 background.png
    "foreground": "$media:foreground"    // 指向 foreground.png
  }
}

// AppScope/resources/base/media/media.json
{
  "media": [
    { "name": "app_icon", "value": "app_icon.png" }   // 传统图标别名
  ]
}
```

#### 图标尺寸规范

| 图片 | 尺寸 | 格式 | 用途 |
|---|---|---|---|
| `background.png` | 1024×1024 | PNG (RGBA) | 背景层，通常是纯色或渐变 |
| `foreground.png` | 2048×1875 | PNG (RGB) | 前景层，包含 logo/图形主体 |
| `foreground_1.png` | 1024×1024 | PNG (RGBA) | 备用前景（可选） |
| `app_icon.png` | 2048×1875 | PNG (RGB) | 传统整图标，不支持分层的设备回退用 |

> **设计要点**：前景层四周需留出安全边距（约 18%），因为系统会对图标进行圆形/圆角裁剪。背景层会被裁剪到设备形状内。

#### 工作原理

```
系统桌面图标渲染流程：

  background.png ─┐
                  ├─→ 系统合成 ─→ 按设备形状裁剪 ─→ 显示
  foreground.png ─┘

  不支持分层图标的设备 → 回退使用 app_icon.png
```

### 11.3 系统层图标 — 启动画面图标

应用冷启动时显示的 Splash 画面中使用的图标。

#### 配置位置

```json5
// entry/src/main/module.json5 → abilities[0]
{
  "name": "EntryAbility",
  "startWindowIcon": "$media:startIcon",              // 启动图标
  "startWindowBackground": "$color:start_window_background"  // 启动背景色
}
```

#### 文件结构

```
entry/src/main/resources/base/media/
├── startIcon.png        # 启动图标（2048×1875, RGB）
├── start_icon.png       # 启动图标源文件（1280×1280, JPEG — 实际尺寸）
└── media.json           # 资源别名映射
```

```json5
// entry/src/main/resources/base/media/media.json
{
  "media": [
    { "name": "startIcon", "value": "start_icon.png" },   // 别名 → 实际文件
    { "name": "app_icon", "value": "app_icon.png" }
  ]
}
```

#### 启动背景色

```json5
// entry/src/main/resources/base/element/color.json（亮色）
{ "name": "start_window_background", "value": "#FFFFFF" }

// entry/src/main/resources/dark/element/color.json（暗色）
{ "name": "start_window_background", "value": "#000000" }
```

系统自动根据用户主题选择亮色或暗色背景。

#### 启动画面渲染流程

```
用户点击应用图标
  → 系统显示 Start Window（启动窗口）
    → 背景：start_window_background 颜色
    → 图标：startIcon 居中显示
  → EntryAbility.onWindowStageCreate() 完成
    → 加载 MainPage
    → 启动窗口消失
```

### 11.4 应用内图标 — Emoji 图标体系

星愿池大量使用 Emoji 作为业务图标（目标、徽章、头像等），这是 HarmonyOS 上最轻量的图标方案。

#### 为什么用 Emoji 而非 SVG/PNG

| 方案 | 优点 | 缺点 |
|---|---|---|
| **Emoji** ✅ | 零资源体积、系统原生支持、色彩丰富 | 样式不可控（随系统字体变化） |
| SVG | 矢量缩放 | HarmonyOS ArkTS 支持有限 |
| PNG | 完全可控 | 体积大、需多倍图适配 |

#### Emoji 工具函数（`common/constants.ets`）

```typescript
/**
 * 判断字符串是否为单个 Emoji
 * 用于头像输入校验 — 只允许单个 Emoji 作为头像
 */
export function isSingleEmoji(str: string): boolean {
  if (!str || str.length === 0) return false;
  const emojiRegex = /\p{Emoji_Presentation}|\p{Emoji}️/u;
  const matches = str.match(emojiRegex);
  if (!matches || matches.length === 0) return false;
  const emojiCount = (str.match(/\p{Emoji_Presentation}|\p{Emoji}️/gu) || []).length;
  const textWithoutEmoji = str.replace(/\p{Emoji_Presentation}|\p{Emoji}️/gu, '').trim();
  return emojiCount === 1 && textWithoutEmoji.length === 0;
}

/**
 * 提取字符串中的第一个 Emoji
 * 用户输入可能包含多余文字，提取有效 Emoji
 */
export function extractFirstEmoji(str: string): string {
  if (!str) return '';
  const emojiRegex = /\p{Emoji_Presentation}|\p{Emoji}️/u;
  const match = str.match(emojiRegex);
  return match ? match[0] : '';
}

/**
 * 安全获取图标显示文本
 * 区分 Emoji 和图片路径，返回适合 Text 组件显示的内容
 */
export function getSafeIconDisplay(icon: string): string {
  if (!icon || icon.length === 0) return '';
  // 图片路径（data:、local://、/ 开头）不是 Emoji，返回空
  if (icon.startsWith('data:') || icon.startsWith('local://') || icon.startsWith('/')) {
    return '';
  }
  return extractFirstEmoji(icon) || '';
}
```

#### Emoji 图标的应用场景

```typescript
// 头像选项 — 固定 Emoji 列表
export const AVATAR_OPTIONS: string[] = ['👧', '👦', '🐱', '🐶'];

// 默认目标 — 每个目标有 icon 字段
{ id: 'g1', title: '整理书桌', icon: '🧹', ... }
{ id: 'g2', title: '整理玩具', icon: '🧸', ... }
{ id: 'g3', title: 'ABC Reading', icon: '📚', ... }

// 内置徽章 — 10 个徽章各有 Emoji 图标
{ id: 'b_streak_3', icon: '🔥', title: '三天打鱼', ... }
{ id: 'b_streak_7', icon: '💪', title: '一周坚持', ... }
{ id: 'b_stars_100', icon: '⭐', title: '百星成就', ... }
{ id: 'b_stars_500', icon: '🏆', title: '五百星大师', ... }
```

### 11.5 应用内图标 — 混合渲染模式（Emoji + 图片）

业务图标（目标、奖励、徽章）的 `icon`/`image` 字段可能存储两种类型：

| 存储值 | 类型 | 渲染方式 |
|---|---|---|
| `'🧹'` / `'⭐'` | Emoji | `Text(icon)` |
| `'local://images/xxx.jpg'` | 本地图片 | `Image(file://path)` |
| `'data:image/jpeg;base64,...'` | Base64 图片 | `Image(dataUri)` |
| `'https://...'` | 网络图片 | `Image(url)` |

#### 组件中的渲染模式

```typescript
// components/GoalCard.ets — 目标卡片
import { getSafeIconDisplay } from '../common/constants';
import { imageStorageService } from '../services/ImageStorageService';

@Component
struct GoalCard {
  goal: Goal = {} as Goal;

  build() {
    Row() {
      // 方案一：图片路径 → 用 Image 组件
      if (imageStorageService.shouldUseImageComponent(this.goal.icon)) {
        Image(imageStorageService.getDisplayPath(this.goal.icon))
          .width(40)
          .height(40)
          .borderRadius(8)
      }
      // 方案二：Emoji → 用 Text 组件
      else {
        Text(getSafeIconDisplay(this.goal.icon) || '🎯')
          .fontSize(32)
      }
    }
  }
}
```

```typescript
// components/RewardCard.ets — 奖励卡片（同样的模式）
if (imageStorageService.shouldUseImageComponent(this.reward.image)) {
  Image(imageStorageService.getDisplayPath(this.reward.image))
    .width(60).height(60).borderRadius(8)
} else {
  Text(getSafeIconDisplay(this.reward.image))
    .fontSize(40)
}
```

#### ImageStorageService 路径转换

```typescript
// services/ImageStorageService.ets

// 存储时：保存为 local:// 格式的相对路径
const localPath = `local://images/goals/${fileName}`;
// 实际存储位置：{filesDir}/images/goals/{fileName}

// 显示时：转换为 file:// 格式的绝对路径
getDisplayPath(imageSource: string): string {
  if (this.isLocalImage(imageSource)) {
    const filePath = this.localPathToFilePath(imageSource);
    return `file://${filePath}`;    // → file:///data/.../files/images/goals/xxx.jpg
  }
  if (this.isBase64Image(imageSource) || this.isNetworkImage(imageSource)) {
    return imageSource;             // 原样返回
  }
  return '';                        // Emoji 返回空，由调用方降级为 Text 渲染
}

// 判断是否应使用 Image 组件
shouldUseImageComponent(imageSource: string): boolean {
  return this.isLocalImage(imageSource)    // local:// 开头
      || this.isBase64Image(imageSource)   // data: 开头
      || this.isNetworkImage(imageSource); // http/https 开头
}
```

#### 完整判断流程

```
icon/image 字段值
  │
  ├─ '🧹' (Emoji)
  │    → getSafeIconDisplay() 返回 '🧹'
  │    → shouldUseImageComponent() 返回 false
  │    → 用 Text('🧹') 渲染
  │
  ├─ 'local://images/goals/abc.jpg' (本地图片)
  │    → getSafeIconDisplay() 返回 ''（过滤掉）
  │    → shouldUseImageComponent() 返回 true
  │    → getDisplayPath() 返回 'file:///data/.../files/images/goals/abc.jpg'
  │    → 用 Image('file://...') 渲染
  │
  ├─ 'data:image/jpeg;base64,...' (Base64)
  │    → shouldUseImageComponent() 返回 true
  │    → getDisplayPath() 返回原始 base64 字符串
  │    → 用 Image('data:...') 渲染
  │
  └─ 'https://example.com/img.png' (网络图片)
       → shouldUseImageComponent() 返回 true
       → getDisplayPath() 返回原始 URL
       → 用 Image('https://...') 渲染
```

### 11.6 本地图片存储目录结构

```
{filesDir}/
└── images/
    ├── avatars/          # 用户头像图片
    ├── goals/            # 目标自定义图标
    ├── rewards/          # 奖励自定义图片
    └── records/          # 成长日记附带照片
```

所有本地图片通过 `ImageStorageService` 管理：
- **保存**：拍照/选图 → 压缩 → 写入 `filesDir/images/{category}/` → 返回 `local://images/{category}/{filename}` 标识
- **显示**：`local://` 标识 → `file://` 绝对路径 → `Image` 组件加载
- **删除**：根据 `local://` 标识定位文件并删除

### 11.7 图标体系设计总结

```
┌─────────────────────────────────────────────────────────────┐
│                     HarmonyOS 图标体系                       │
├──────────────┬──────────────┬───────────────────────────────┤
│   系统图标    │   启动图标    │        应用内业务图标           │
├──────────────┼──────────────┼───────────────────────────────┤
│ layered_image│ startIcon    │  Emoji(Text) + Image(图片)    │
│ .json 配置   │ 模块 media   │  混合渲染                      │
├──────────────┼──────────────┼───────────────────────────────┤
│ background   │ start_icon   │  getSafeIconDisplay()         │
│ .png (背景)  │ .png         │  shouldUseImageComponent()    │
│ foreground   │              │  getDisplayPath()             │
│ .png (前景)  │              │                               │
├──────────────┼──────────────┼───────────────────────────────┤
│ AppScope/    │ entry/       │  common/constants.ets         │
│ resources/   │ resources/   │  services/ImageStorageService │
│ base/media/  │ base/media/  │  components/*.ets             │
└──────────────┴──────────────┴───────────────────────────────┘

---

## 十四、应用上架合规检查清单

提交应用市场审核前，逐项检查以下合规项：

### 14.1 设备类型（module.json5）

```
□ deviceTypes 字段不为空
□ 不包含 "default" 值
□ 至少声明一个真实设备类型（通常为 "phone"）
□ 声明的设备类型都做过真机适配测试
```

### 14.2 深色模式（颜色资源）

```
□ 所有颜色通过 $r('app.color.xxx') 引用，无硬编码十六进制值
□ 所有颜色在 base/color.json 和 dark/color.json 中都有定义
□ 页面背景、卡片背景、文字颜色在深色模式下对比度足够
□ 弹窗、遮罩在深色模式下视觉正常
```

### 14.3 应用身份（app.json5）

```
□ bundleName 使用反向域名格式且全网唯一
□ versionCode 比上一版本递增
□ versionName 与 versionCode 对应关系正确
□ 图标文件存在且尺寸正确（layered_image 引用的 background/foreground）
```

### 14.4 签名与构建（build-profile.json5）

```
□ 使用发布证书（release）签名，非调试证书
□ signingConfigs 中的证书文件路径有效
□ targetSdkVersion ≥ compatibleSdkVersion
□ modules[] 中模块名与目录名一致
```

### 14.5 权限声明（module.json5）

```
□ 所有 requestPermissions 都有 reason 字段（敏感权限必须有）
□ reason 文字清晰说明用途，不含模板占位符
□ usedScene.when 使用正确（inuse vs always）
□ 没有声明实际未使用的权限
```

### 14.6 资源完整性

```
□ startWindowIcon 指向的图标文件存在
□ startWindowBackground 指向的颜色值在 color.json 中存在
□ main_pages.json 中注册的页面文件都存在
□ $media: / $string: / $color: / $profile: 引用全部可解析
```

---

## 十五、鸿蒙应用 UX 设计规范（上架审核核心）

> 参考：[华为开发者文档 — 应用 UX 设计规范](https://developer.huawei.com/consumer/cn/doc/app/50104)
> 以下规范为应用市场上架审核的核心检查项，未通过将直接被拒。

### 15.1 应用结构规范

#### 15.1.1 页面布局原则

```
┌──────────────────────────────────┐
│  状态栏（系统托管，应用不可修改）    │  高度：系统自动
├──────────────────────────────────┤
│  标题栏 / 导航栏                  │  应用自定义，但需遵循规范高度
├──────────────────────────────────┤
│                                  │
│  内容区域                         │  可滚动、可交互
│                                  │
├──────────────────────────────────┤
│  底部导航栏 / TabBar             │  应用自定义，遵循规范高度
└──────────────────────────────────┘
```

**硬性规则：**
- 状态栏区域**禁止放置任何可交互元素**（按钮、链接等）
- 内容不得被状态栏、刘海屏、圆角遮挡
- 底部安全区域（手势指示器区域）禁止放置关键操作按钮

#### 15.1.2 导航规范

| 导航类型 | 适用场景 | 规范要求 |
|---|---|---|
| TabBar 导航 | 一级页面切换（≤5 个） | 底部固定，图标+文字，当前项高亮 |
| 侧边导航 | 二级/设置页面 | 从左侧滑入，支持手势返回 |
| 栈导航 | 详情/编辑页面 | 支持左滑返回手势，有明确返回按钮 |

```typescript
// ✅ 正确：TabBar 底部导航
TabBar({ currentTab: this.currentTab, onChange: (t) => this.currentTab = t })

// ❌ 错误：自定义手势与系统返回手势冲突
// 避免在页面左侧边缘定义与系统返回手势冲突的交互
```

#### 15.1.3 弹窗规范

```typescript
// ✅ 正确：弹窗必须有明确的关闭方式
@Builder
DialogBuilder() {
  Column() {
    // 内容...
    Button('取消').onClick(() => this.closeDialog())  // 明确关闭按钮
    Button('确定').onClick(() => this.confirm())
  }
}

// ❌ 错误：弹窗没有关闭途径，用户无法退出
```

**弹窗规则：**
- 每个弹窗必须有明确的关闭方式（取消按钮、关闭图标、点击遮罩关闭）
- 弹窗内容超出屏幕时必须可滚动
- 全屏弹窗必须提供返回/关闭按钮
- 确认类弹窗（删除、支付等）必须有二次确认

---

### 15.2 色彩规范

#### 15.2.1 色彩体系

HarmonyOS Design 定义了标准色彩语义，应用应遵循：

| 色彩角色 | 用途 | 亮色模式 | 深色模式 |
|---|---|---|---|
| 主色调 | 品牌色、主操作 | 应用自定义 | 保持一致或略调亮 |
| 背景色-一级 | 页面主背景 | `#F8FAFC` | `#0F172A` |
| 背景色-二级 | 卡片/容器 | `#FFFFFF` | `#1E293B` |
| 文字色-一级 | 标题/正文 | `#1E293B` | `#F1F5F9` |
| 文字色-二级 | 次要信息 | `#64748B` | `#94A3B8` |
| 文字色-三级 | 提示/占位 | `#94A3B8` | `#64748B` |
| 分割线 | 区域分隔 | `#E2E8F0` | `#334155` |
| 成功色 | 正向反馈 | `#10B981` | `#10B981` |
| 警告色 | 注意提示 | `#F59E0B` | `#F59E0B` |
| 错误色 | 负面反馈 | `#EF4444` | `#EF4444` |

#### 15.2.2 对比度要求（WCAG 2.1 AA）

文字与背景的对比度必须满足最低标准：

| 场景 | 最低对比度 | 说明 |
|---|---|---|
| 正文文字（≥16sp） | 4.5:1 | 标签、说明文字 |
| 大号文字（≥18sp 粗体 或 ≥24sp） | 3:1 | 标题、大按钮文字 |
| 图标/图形元素 | 3:1 | 功能性图标 |

```typescript
// ❌ 低对比度 — 浅灰文字在白色背景上几乎不可见
.fontColor('#D1D5DB')     // 对比度约 1.5:1
.backgroundColor('#FFFFFF')

// ✅ 足够对比度
.fontColor($r('app.color.text_secondary'))   // #64748B 对比度约 4.6:1
.backgroundColor($r('app.color.bg_card'))
```

**自查工具**：使用 DevEco Studio 的 Accessibility Inspector 或在线对比度检查器验证。

---

### 15.3 深色模式适配（强制要求）

> 深色模式未适配是上架被拒的最常见原因之一。

#### 15.3.1 适配原则

```
深色模式 ≠ 简单颜色反转

正确做法：
  亮色背景 #FFFFFF → 深色背景 #1E293B（深蓝灰，非纯黑）
  亮色文字 #1E293B → 深色文字 #F1F5F9（浅灰白，非纯白）

错误做法：
  亮色 #FFFFFF → 深色 #000000（纯黑导致 OLED 眩光）
  亮色 #000000 → 深色 #FFFFFF（纯白文字刺眼）
```

#### 15.3.2 适配清单

```
□ 页面背景色：base #F8FAFC ↔ dark #0F172A
□ 卡片背景色：base #FFFFFF ↔ dark #1E293B
□ 主文字色：base #1E293B ↔ dark #F1F5F9
□ 次文字色：base #64748B ↔ dark #94A3B8
□ 输入框背景：base #F8FAFC ↔ dark #334155
□ 分割线：base #E2E8F0 ↔ dark #334155
□ 弹窗遮罩：base #80000000 ↔ dark #CC000000
□ 弹窗背景：base #FFFFFF ↔ dark #1E293B
□ 状态栏：跟随系统自动切换
□ 图片/图标：非必要不调整，但需确保深色背景上可见
□ 阴影：深色模式下阴影不可见，改用边框或亮度差区分层级
```

#### 15.3.3 禁止事项

```typescript
// ❌ 禁止：强制覆盖系统主题
AppStorage.SetOrCreate('colorMode', ConfigurationConstant.ColorMode.COLOR_MODE_LIGHT)

// ❌ 禁止：硬编码颜色绕过深色模式
.fontColor('#1E293B')  // 深色模式下仍然是深色文字，不可见

// ❌ 禁止：图片上有白色文字，深色模式下图片变暗导致文字不可见
// 解决：图片上叠加半透明遮罩
```

---

### 15.4 字体与排版规范

#### 15.4.1 字号规范

| 层级 | 字号 | 字重 | 用途 |
|---|---|---|---|
| H1 | 28sp | Bold | 页面主标题 |
| H2 | 22sp | Bold | 区域标题 |
| H3 | 18sp | Medium | 卡片标题 |
| Body1 | 16sp | Regular | 正文内容 |
| Body2 | 14sp | Regular | 辅助说明 |
| Caption | 12sp | Regular | 时间戳、标签 |

```typescript
// ✅ 正确：使用 sp 单位（随系统字号缩放）
Text('标题').fontSize(22)           // 默认 sp
Text('正文').fontSize(16)

// ❌ 错误：使用 fp 或 px（不随系统设置缩放）
Text('标题').fontSize('22fp')
```

#### 15.4.2 行高与间距

```typescript
// ✅ 正确：正文行高 1.5 倍
Text('正文内容')
  .fontSize(16)
  .lineHeight(24)     // 16 × 1.5 = 24

// ✅ 正确：段落间距
Column({ space: 16 }) {   // 段落间距 16vp
  Text('段落一')
  Text('段落二')
}
```

#### 15.4.3 文字截断与换行

```typescript
// ✅ 正确：超长文字省略号截断
Text('很长很长的标题文字...')
  .maxLines(1)
  .textOverflow({ overflow: TextOverflow.Ellipsis })

// ✅ 正确：多行内容限制
Text('描述文字...')
  .maxLines(3)
  .textOverflow({ overflow: TextOverflow.Ellipsis })

// ❌ 错误：文字溢出容器导致布局错乱
Text('很长很长的标题').width(100)  // 无截断设置，文字会溢出
```

---

### 15.5 交互规范

#### 15.5.1 触摸热区

```
最小触摸目标尺寸：48vp × 48vp
推荐触摸目标间距：8vp

┌─────────────────────────────┐
│         48vp × 48vp         │  ← 最小可点击区域
│    ┌───────────────────┐    │
│    │   实际按钮内容     │    │
│    └───────────────────┘    │
│         8vp 间距            │  ← 与相邻元素的距离
│    ┌───────────────────┐    │
│    │   下一个按钮       │    │
│    └───────────────────┘    │
└─────────────────────────────┘
```

```typescript
// ❌ 错误：按钮太小，用户难以点击
Button('×')
  .width(20)
  .height(20)

// ✅ 正确：最小触摸区域 48vp
Button('×')
  .width(48)
  .height(48)
  .fontSize(16)
```

#### 15.5.2 反馈机制

| 交互 | 必须有反馈 | 实现方式 |
|---|---|---|
| 按钮点击 | 视觉反馈 | 状态变化（颜色/透明度/缩放） |
| 长按 | 触觉反馈 | `vibrator.vibrate()` |
| 操作成功 | 提示 | Toast / Snackbar |
| 操作失败 | 提示 | Toast / Dialog |
| 加载中 | 进度指示 | Loading 组件 |
| 空状态 | 引导 | 空状态插图 + 引导文字 |

```typescript
// ✅ 正确：操作反馈完整
Button('保存')
  .onClick(() => {
    this.saving = true;  // 显示加载状态
    dataStore.saveData(this.data)
      .then(() => {
        promptAction.showToast({ message: '保存成功' });  // 成功反馈
      })
      .catch(() => {
        promptAction.showToast({ message: '保存失败，请重试' });  // 失败反馈
      })
      .finally(() => {
        this.saving = false;
      });
  })
```

#### 15.5.3 手势规范

| 手势 | 系统保留 | 应用可使用 |
|---|---|---|
| 左滑从边缘 | **系统返回手势** | 页面内部左滑操作（非边缘） |
| 下拉状态栏 | **系统通知中心** | 页面内部下拉刷新（非顶部边缘） |
| 长按 | 系统复制（文字选中时） | 自定义长按菜单 |

```typescript
// ❌ 错误：在页面边缘定义左滑操作，与系统返回手势冲突
.gesture(
  PanGesture({ direction: PanDirection.Left })
    .onActionStart(() => { /* 从左边缘开始的滑动会被系统拦截 */ })
)

// ✅ 正确：在内容区域定义滑动操作
.gesture(
  PanGesture({ direction: PanDirection.Left })
    .onActionStart(() => { /* 只在内容区域生效 */ })
)
```

---

### 15.6 图片与媒体规范

#### 15.6.1 图片加载与占位

```typescript
// ✅ 正确：图片加载有占位和错误处理
Image(this.imageUrl)
  .width(100)
  .height(100)
  .borderRadius(8)
  .placeholder($r('app.media.placeholder'))   // 加载中占位图
  .onError(() => { this.imageError = true; }) // 加载失败处理

// ❌ 错误：图片加载失败显示空白或破碎图标
Image(this.imageUrl)
  .width(100)
  .height(100)
  // 无 placeholder、无 onError
```

#### 15.6.2 图片适配

```typescript
// ✅ 正确：使用 ObjectFit 适配不同比例
Image($r('app.media.banner'))
  .width('100%')
  .height(200)
  .objectFit(ImageFit.Cover)    // 裁剪填充，保持比例

// ❌ 错误：拉伸变形
Image($r('app.media.banner'))
  .width('100%')
  .height(200)
  // 默认 Fill 模式会拉伸变形
```

---

### 15.7 性能规范

#### 15.7.1 启动性能

| 指标 | 要求 | 说明 |
|---|---|---|
| 冷启动时间 | ≤ 2 秒 | 从点击图标到首页可交互 |
| 热启动时间 | ≤ 1 秒 | 从后台恢复到可交互 |

```typescript
// ✅ 正确：延迟加载非关键数据
aboutToAppear() {
  // 立即加载关键数据
  this.loadUserData();

  // 延迟加载非关键数据
  setTimeout(() => {
    this.loadBadges();
    this.loadTemplates();
  }, 500);
}
```

#### 15.7.2 列表性能

```typescript
// ✅ 正确：使用 LazyForEach 懒加载
List() {
  LazyForEach(this.dataSource, (item: Goal) => {
    ListItem() {
      GoalCard({ goal: item })
    }
  }, (item: Goal) => item.id)   // 必须提供唯一 key
}

// ❌ 错误：ForEach 一次性渲染所有数据
List() {
  ForEach(this.goals, (item: Goal) => {
    ListItem() {
      GoalCard({ goal: item })
    }
  })
}
```

#### 15.7.3 内存管理

```typescript
// ✅ 正确：页面销毁时释放资源
aboutToDisappear() {
  // 取消定时器
  if (this.timer) {
    clearInterval(this.timer);
  }
  // 取消订阅
  this.unsubscribe();
}
```

---

### 15.8 无障碍规范

#### 15.8.1 基本要求

```typescript
// ✅ 正确：为交互元素添加无障碍描述
Button('删除')
  .accessibilityText('删除目标：整理书桌')   // 屏幕阅读器会读出

// ✅ 正确：装饰性图片标记为无语义
Image($r('app.media.decoration'))
  .accessibilityLevel('no')   // 屏幕阅读器跳过

// ❌ 错误：纯图标按钮没有文字描述
Button()
  .icon($r('app.media.ic_delete'))
  // 没有 accessibilityText，屏幕阅读器无法识别
```

---

### 15.9 应用图标规范

#### 15.9.1 图标设计要求

| 要求 | 说明 |
|---|---|
| 形状 | 系统自动裁剪为超椭圆（Squircle），设计时需预留安全边距 |
| 尺寸 | 设计稿 1024×1024px，导出 2048×2048px 前景层 |
| 安全区域 | 四周预留 18% 边距，确保裁剪后核心内容完整 |
| 背景 | 纯色或简单渐变，避免复杂图案（裁剪后可能丢失细节） |
| 前景 | Logo/图形主体，居中放置 |
| 文字 | 不建议在图标中放文字（小尺寸下不可读） |

```
┌──────────────────────────────┐
│      18% 安全边距             │
│   ┌──────────────────────┐   │
│   │                      │   │
│   │    核心图标内容        │   │
│   │    （超椭圆裁剪区域内）│   │
│   │                      │   │
│   └──────────────────────┘   │
│      18% 安全边距             │
└──────────────────────────────┘
         1024 × 1024 设计稿
```

---

### 15.10 审核常见被拒原因速查

| 被拒原因 | 涉及章节 | 修复方法 |
|---|---|---|
| 深色模式未适配 | 15.3 | 所有颜色改为资源引用，补充 dark/color.json |
| deviceTypes 不合规 | 11.3.1a | 移除 `default`，使用 `phone` 等真实值 |
| 图标不合规 | 15.9 | 遵循安全区域规范，避免文字 |
| 对比度不足 | 15.2.2 | 使用对比度检查工具验证 |
| 触摸热区太小 | 15.5.1 | 最小 48vp × 48vp |
| 弹窗无法关闭 | 15.1.3 | 添加取消/关闭按钮 |
| 权限未说明 | 11.3.3 | 补充 reason 字段 |
| 启动过慢 | 15.7.1 | 延迟加载非关键数据 |
| 文字溢出 | 15.4.3 | 添加 maxLines + Ellipsis |
| 空状态无引导 | 15.5.2 | 添加空状态插图和引导文字 |
```
