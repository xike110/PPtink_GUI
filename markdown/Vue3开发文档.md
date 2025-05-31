# PPtink桌面GUI框架 Vue3开发文档

## 项目概述
本项目使用Vue3 + TypeScript + Vite构建桌面应用的WebView界面，采用现代化的前端技术栈和最佳实践。

## 技术栈
- Vue 3.5.13
- TypeScript
- Vite 6.2.0
- Vue Router 4.5.0
- Pinia 3.0.1
- SASS
- Lucide Vue Next (图标库)

## 项目结构
```
vuecode/
├── src/                    # 源代码目录
│   ├── assets/            # 静态资源
│   ├── components/        # 组件目录
│   ├── router/           # 路由配置
│   ├── App.vue           # 根组件
│   ├── main.ts           # 入口文件
│   └── style.css         # 全局样式
├── public/                # 公共资源
├── dist/                  # 构建输出目录
├── vite.config.ts        # Vite配置
└── package.json          # 项目配置
```

## 开发环境设置
1. 安装依赖
```bash
npm install
```

2. 开发服务器
```bash
npm run dev
```

3. 构建生产版本
```bash
npm run build
```

## 核心功能

### 1. 主题系统
- 支持亮色/暗色主题切换
- 主题状态持久化存储
- 响应式主题切换

```typescript
// 主题切换实现
const currentTheme = ref('light');
const toggleTheme = (theme: string) => {
  currentTheme.value = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
};
```

### 2. 窗口控制
- 最小化
- 关闭
- 全屏切换

```typescript
// 窗口控制函数
function minimize() {
  pywebview.api.minimize();
}

function destroy() {
  pywebview.api.destroy();
}

function toggle_fullscreen() {
  pywebview.api.toggle_fullscreen();
}
```

### 3. 导航系统
- 响应式侧边栏
- 路由导航
- 图标集成

```vue
<template>
  <div class="nav-items">
    <router-link class="nav-item" to="/">
      <UserIcon class="nav-icon" />
      <span>软件主页</span>
    </router-link>
    <!-- 其他导航项 -->
  </div>
</template>
```

## 组件开发规范

### 1. 组件命名
- 使用PascalCase命名组件
- 组件文件名与组件名保持一致

### 2. 组件结构
```vue
<template>
  <!-- 模板部分 -->
</template>

<script setup lang="ts">
// 逻辑部分
</script>

<style lang="scss" scoped>
// 样式部分
</style>
```

### 3. Props定义
```typescript
interface Props {
  title: string;
  type?: 'primary' | 'secondary';
}

const props = withDefaults(defineProps<Props>(), {
  type: 'primary'
});
```

## 状态管理

### 1. Pinia Store
```typescript
// stores/app.ts
import { defineStore } from 'pinia';

export const useAppStore = defineStore('app', {
  state: () => ({
    theme: 'light',
    userInfo: null
  }),
  actions: {
    setTheme(theme: string) {
      this.theme = theme;
    }
  }
});
```

## 路由配置

### 1. 路由定义
```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/chat',
    component: () => import('../views/Chat.vue')
  }
];

export const router = createRouter({
  history: createWebHistory(),
  routes
});
```

## 样式指南

### 1. SCSS变量
```scss
// 主题变量
$primary-color: #031C25;
$body-color: #16232F;
$text-color: #333;
$border-color: #e8e8e8;
```

### 2. 响应式设计
```scss
// 响应式断点
$breakpoints: (
  'sm': 576px,
  'md': 768px,
  'lg': 992px,
  'xl': 1200px
);

// 响应式混入
@mixin responsive($breakpoint) {
  @media (min-width: map-get($breakpoints, $breakpoint)) {
    @content;
  }
}
```

## 与Python交互

### 1. PyWebView API
```typescript
// 检查API可用性
const isPywebviewReady = ref(false);

onMounted(() => {
  const checkReady = () => {
    if (window.pywebview && window.pywebview.api) {
      isPywebviewReady.value = true;
    } else {
      setTimeout(checkReady, 100);
    }
  };
  checkReady();
});
```

### 2. 日志系统
```typescript
function log(level: string, message: string) {
  pywebview.api.log(level, message);
  console.log(level, message);
}
```

## 性能优化

### 1. 组件懒加载
```typescript
const AsyncComponent = defineAsyncComponent(() =>
  import('./components/Heavy.vue')
);
```

### 2. 图片优化
- 使用适当的图片格式
- 实现懒加载
- 使用响应式图片

## 调试指南

### 1. Vue DevTools
- 安装Vue DevTools浏览器扩展
- 使用组件检查器
- 状态管理调试

### 2. 控制台调试
```typescript
// 开发环境日志
if (import.meta.env.DEV) {
  console.log('调试信息');
}
```

## 部署说明

### 1. 构建配置
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true
  }
});
```

### 2. 环境变量
```env
VITE_API_URL=http://localhost:3000
VITE_APP_TITLE=PPtink
```

## 常见问题

### 1. 主题切换问题
- 检查localStorage权限
- 验证CSS变量定义
- 确认主题切换事件触发

### 2. 路由问题
- 检查路由配置
- 验证组件导入
- 确认路由守卫设置

### 3. API通信问题
- 检查PyWebView初始化
- 验证API方法调用
- 确认数据格式匹配 