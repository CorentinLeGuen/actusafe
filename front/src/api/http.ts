import type {Article} from "./schemas.ts";


export async function getArticles(): Promise<Article[]> {
    const res = await fetch('http://localhost:8000/articles', {method: 'GET'})
    return await res.json()
}