import type {Article, Category, Source} from "./schemas.ts";


export async function getArticles(): Promise<Article[]> {
    const res = await fetch('http://localhost:8000/articles', {method: 'GET'})
    return await res.json()
}

export async function getCategories(): Promise<Category[]> {
    const res = await fetch('http://localhost:8000/categories', {method: 'GET'})
    return await res.json()
}

export async function getSources(): Promise<Source[]> {
    const res = await fetch('http://localhost:8000/sources', {method: 'GET'})
    return await res.json()
}
