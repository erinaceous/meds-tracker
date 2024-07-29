import exp from "node:constants";

export default defineNuxtPlugin(() => {
    return {
        provide: {
            localStorage: {
                getItem(item: string) {
                    if (import.meta.client) {
                        let val = localStorage.getItem(item);
                        try {
                            let obj = JSON.parse(val)
                            if (obj.expires_at) {
                                let expires_at = new Date(obj.expires_at);
                                let now = new Date();
                                if (now > expires_at) {
                                    return undefined
                                }
                            }
                            return obj?.value
                        } catch {
                            return val
                        }
                    } else {
                        return undefined
                    }
                },
                setItem(item: string, value: any, expires_at: Date | undefined = undefined) {
                    if (import.meta.client) {
                        if (expires_at && !(expires_at instanceof Date)) {
                            expires_at = new Date(expires_at);
                        }
                        return localStorage.setItem(item, JSON.stringify({
                            "value": value,
                            "expires_at": expires_at?.toUTCString()
                        }))
                    }
                },
                removeItem(item: string) {
                    if (import.meta.client) {
                        localStorage.removeItem(item)
                    }
                }
            }
        }
    }
})