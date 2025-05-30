<template>
  <div class="about">
    <a-card :bordered="false">
      <template #title>关于系统</template>
      <p>这是一个基于 Vue 3 + Ant Design Vue 的股票行情系统。</p>
      <p>系统特点：</p>
      <ul>
        <li>实时行情展示</li>
        <li>K线图分析</li>
        <li>交易数据统计</li>
        <li>响应式设计</li>
      </ul>
      <p>技术栈：</p>
      <ul>
        <li>Vue 3</li>
        <li>Ant Design Vue</li>
        <li>Vue Router</li>
        <li>Vite</li>
      </ul>
    </a-card>
  </div>
</template>

<style scoped>
.about {
  margin: 0 auto;
  padding: 0 16px;
}

p {
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.6;
}

ul {
  color: rgba(255, 255, 255, 0.85);
  padding-left: 20px;
}

li {
  margin: 8px 0;
}
</style> 