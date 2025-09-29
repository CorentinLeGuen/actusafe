<script setup lang="ts">
import {onMounted, ref} from "vue";
import {initFlowbite} from "flowbite";
import {getArticles, getCategories} from "./api/http.ts";
import type {Article, Category} from "./api/schemas.ts";

const articles = ref<Article[]>([])
const categories = ref<Category[]>([])

async function fetchArticles() {
  articles.value = await getArticles()
}

async function fetchCategories() {
  categories.value = await getCategories()
}

onMounted(async () => {
  await fetchCategories()
  await fetchArticles()
  initFlowbite()
})
</script>

<template>
  <div class="h-screen p-4">
    <h1 class="font-extrabold drop-shadow-sm/30 text-center text-8xl"><span class="text-transparent bg-clip-text bg-gradient-to-r to-[#FFC29B] from-[#B95E82]">ActuSafe</span></h1>
    <p class="text-center text-gray-700 font-extralight text-2xl mb-4">Les actualités en toute sécurité</p>
    <div class="flex flex-justify-center flex-wrap mb-4 space-y-2 max-w-4/5 mx-auto">
      <span v-for="category in categories" class="flex-auto text-center mx-1 bg-gray-100 text-gray-700 text-xs font-medium me-2 rounded-lg px-1 h-4.5 hover:bg-gray-50 hover:cursor-pointer">
        {{category.name}}
      </span>
    </div>
    <div class="flex flex-wrap gap-2 justify-center">
      <div v-for="article in articles" class="w-1/5 hover:cursor-pointer">
        <a :href="article.origin_url" target="_blank">
          <img :src="article.thumbnail" alt="Article thumbnail" class="w-full rounded-t-xl h-[240px]">
          <h2 class="font-extrabold text-center text-xl">{{ article.article_name }}</h2>
          <p class="text-sm text-gray-600">{{ article.subtitle }}</p>
          <p class="text-gray-800">{{ article.lead_text }}</p>
          <p v-for="category in article.categories" class="text-sm"><span class="px-2 py-0.5 text-xs rounded bg-[#FFECC0] text-gray-500">{{ category.name }}</span></p>
          <p class="text-xs text-right text-gray-400">{{ article.publish_date }}<span v-if="article.updated_at"> | {{ article.updated_at }}</span></p>
          <p class="text-xs text-gray-400">{{ article.source.name }}</p>
        </a>
      </div>
    </div>
  </div>
</template>

