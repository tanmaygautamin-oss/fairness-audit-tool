// api.js
// WHAT: Small helper module that wraps all calls to our FastAPI backend,
// so components never need to know the raw URL/axios details directly.

import axios from "axios";

const BASE_URL = "http://localhost:8000";

export async function runAudit(sensitiveAttribute) {
    const response = await axios.post(`${BASE_URL}/api/audit`, {
        sensitive_attribute: sensitiveAttribute
    });
    return response.data;
}

export async function runMitigation(sensitiveAttribute) {
    const response = await axios.post(`${BASE_URL}/api/mitigate`, {
        sensitive_attribute: sensitiveAttribute
    });
    return response.data;
}

