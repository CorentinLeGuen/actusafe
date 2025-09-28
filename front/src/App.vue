<script setup lang="ts">
import {onMounted, ref} from "vue";
import {initFlowbite} from "flowbite";
import {getArticles} from "./api/http.ts";
import type {Article} from "./api/schemas.ts";

const articles = ref<Article[]>([])

async function fetchArticles() {
  articles.value = await getArticles()
}

onMounted(async () => {
  await fetchArticles()
  initFlowbite()
})
</script>

<template>
  <div class="h-screen p-4">
    <h1 class="font-extrabold drop-shadow-sm/30 text-center text-4xl mb-4"><span class="text-transparent bg-clip-text bg-gradient-to-r to-[#FFC29B] from-[#B95E82]">ActuSafe</span></h1>
    <div class="flex flex-wrap gap-2 justify-center">
      <div v-for="article in articles" class="w-1/5 hover:cursor-pointer">
        <a :href="article.origin_url" target="_blank">
          <img :src="article.thumbnail" alt="Article thumbnail" class="w-full rounded-t-xl">
          <h2 class="font-extrabold text-center text-xl">{{ article.article_name }}</h2>
          <p class="text-sm text-gray-600">{{ article.subtitle }}</p>
          <p class="text-gray-800">{{ article.lead_text }}</p>
          <p v-for="category in article.categories" class="text-sm">{{ category.name }}</p>
          <p class="text-xs text-right text-gray-400">{{ article.publish_date }}<span v-if="article.updated_at"> | {{ article.updated_at }}</span></p>
          <p class="text-xs text-gray-400">{{ article.source.name }}</p>
        </a>
      </div>
    </div>
  </div>
</template>

