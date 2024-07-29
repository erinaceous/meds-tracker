import exp from "node:constants";
import createClient from "openapi-fetch";
import type { paths } from "~/api/v0.d.ts";

export default defineNuxtPlugin(() => {
    return {
        provide: {
            api: {
                root: useRuntimeConfig().public.api.root,
                client: createClient<paths>({ baseUrl: useRuntimeConfig().public.api.root })
            }
        }
    }
})