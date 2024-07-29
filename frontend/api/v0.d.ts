/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
    "/altcha/challenge": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Altcha Challenge */
        get: operations["altcha_challenge_altcha_challenge_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/altcha/verify": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Altcha Validate */
        post: operations["altcha_validate_altcha_verify_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/medications": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Medications */
        get: operations["list_medications_medications_get"];
        put?: never;
        /** Submit Medication */
        post: operations["submit_medication_medications_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/medications/autocomplete/{text}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Autocomplete Medications */
        get: operations["autocomplete_medications_medications_autocomplete__text__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/medications/{uid}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Medication */
        get: operations["get_medication_medications__uid__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/medications/{uid}/dosages": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Medication Dosages */
        get: operations["get_medication_dosages_medications__uid__dosages_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/medications/{uid}/types": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Medication Types */
        get: operations["get_medication_types_medications__uid__types_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/pharmacies": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Pharmacies */
        get: operations["list_pharmacies_pharmacies_get"];
        put?: never;
        /** Submit Pharmacy */
        post: operations["submit_pharmacy_pharmacies_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/pharmacies/autocomplete/{postcode}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Autocomplete Pharmacies */
        get: operations["autocomplete_pharmacies_pharmacies_autocomplete__postcode__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/pharmacies/{uid}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Medication */
        get: operations["get_medication_pharmacies__uid__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/reports": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Reports */
        get: operations["get_reports_reports_get"];
        put?: never;
        /** Submit Reports */
        post: operations["submit_reports_reports_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/reports/counts": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Counts */
        get: operations["get_counts_reports_counts_get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /**
         * Algorithm
         * @constant
         * @enum {string}
         */
        Algorithm: "SHA-256";
        /** Altcha */
        Altcha: {
            /** @default SHA-256 */
            algorithm: components["schemas"]["Algorithm"];
            /** Challenge */
            challenge: string;
            /** Salt */
            salt: string;
            /** Number */
            number?: number | null;
            /** Signature */
            signature: string;
            /** Expires */
            expires?: string | null;
            /**
             * Verified
             * @default false
             */
            verified: boolean;
            /** Active */
            readonly active: boolean;
        };
        /** AltchaPayload */
        AltchaPayload: {
            /** Payload */
            payload: string;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** InputMedication */
        InputMedication: {
            /** Category */
            category: string;
            /** Product */
            product?: string | null;
        };
        /** InputPharmacy */
        InputPharmacy: {
            /** Name */
            name: string;
            /** Postcode */
            postcode: string;
            /** Address */
            address: string;
            /** Latitude */
            latitude?: number | null;
            /** Longitude */
            longitude?: number | null;
        };
        /** InputReport */
        InputReport: {
            /** Medication Uid */
            medication_uid: string;
            /** Pharmacy Uid */
            pharmacy_uid: string;
            /** Type */
            type?: string | null;
            /** Dosage */
            dosage?: string | null;
            /** In Stock */
            in_stock: boolean;
            /**
             * Reported On
             * Format: date
             */
            reported_on?: string;
        };
        /** Medication */
        Medication: {
            /** Category */
            category: string;
            /** Product */
            product?: string | null;
            /** Uid */
            uid: string;
        };
        /** Pharmacy */
        Pharmacy: {
            /** Name */
            name: string;
            /** Postcode */
            postcode: string;
            /** Address */
            address: string;
            /** Latitude */
            latitude?: number | null;
            /** Longitude */
            longitude?: number | null;
            /** Uid */
            uid: string;
        };
        /** Report */
        Report: {
            /** Medication Uid */
            medication_uid: string;
            /** Pharmacy Uid */
            pharmacy_uid: string;
            /** Type */
            type?: string | null;
            /** Dosage */
            dosage?: string | null;
            /** In Stock */
            in_stock: boolean;
            /**
             * Reported On
             * Format: date
             */
            reported_on?: string;
            /**
             * Uuid
             * Format: uuid
             */
            uuid?: string;
            /** Signature */
            signature: string;
        };
        /** ReportError */
        ReportError: {
            /** Details */
            details: string;
        };
        /** ReportOutput */
        ReportOutput: {
            /** Report */
            report: components["schemas"]["Report"] | components["schemas"]["InputReport"] | null;
            /**
             * Changed
             * @default true
             */
            changed: boolean;
            error?: components["schemas"]["ReportError"] | null;
        };
        /** ValidationError */
        ValidationError: {
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    altcha_challenge_altcha_challenge_get: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Altcha"];
                };
            };
        };
    };
    altcha_validate_altcha_verify_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AltchaPayload"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Altcha"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_medications_medications_get: {
        parameters: {
            query?: {
                categories?: string[] | null;
                products?: string[] | null;
                uids?: string[] | null;
                start_from?: string | null;
                order?: "asc" | "desc";
                order_by?: "product" | "category" | "uid";
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Medication"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    submit_medication_medications_post: {
        parameters: {
            query?: never;
            header?: {
                authorization?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["InputMedication"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    autocomplete_medications_medications_autocomplete__text__get: {
        parameters: {
            query?: {
                order?: "asc" | "desc";
                order_by?: "product" | "category" | "uid";
            };
            header?: never;
            path: {
                text: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Medication"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_medication_medications__uid__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                uid: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Medication"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_medication_dosages_medications__uid__dosages_get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                uid: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": string[];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_medication_types_medications__uid__types_get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                uid: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": string[];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_pharmacies_pharmacies_get: {
        parameters: {
            query?: {
                latitude?: number | null;
                longitude?: number | null;
                radius?: number | null;
                postcodes?: string[] | null;
                uids?: string[] | null;
                start_from?: string | null;
                order?: "asc" | "desc";
                order_by?: "distance" | "name" | "postcode" | "address" | "uid";
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Pharmacy"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    submit_pharmacy_pharmacies_post: {
        parameters: {
            query?: never;
            header?: {
                authorization?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["InputPharmacy"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Pharmacy"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    autocomplete_pharmacies_pharmacies_autocomplete__postcode__get: {
        parameters: {
            query?: {
                order?: "asc" | "desc";
                order_by?: "distance" | "name" | "postcode" | "address" | "uid";
            };
            header?: never;
            path: {
                postcode: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Pharmacy"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_medication_pharmacies__uid__get: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                uid: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Pharmacy"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_reports_reports_get: {
        parameters: {
            query?: {
                latitude?: number | null;
                longitude?: number | null;
                radius?: number | null;
                max_age?: number | null;
                medications?: string[] | null;
                pharmacies?: string[] | null;
                dosages?: string[] | null;
                types?: string[] | null;
                start_from?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Report"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    submit_reports_reports_post: {
        parameters: {
            query?: never;
            header?: {
                authorization?: string | null;
            };
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["InputReport"][];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ReportOutput"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_counts_reports_counts_get: {
        parameters: {
            query: {
                latitude: number | null;
                longitude: number | null;
                radius?: number | null;
                max_age?: number | null;
                medications?: string[] | null;
                pharmacies?: string[] | null;
                dosages?: string[] | null;
                types?: string[] | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Report"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
}
