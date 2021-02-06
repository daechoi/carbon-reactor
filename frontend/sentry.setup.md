# Using yarn

yarn add @sentry/react @sentry/tracing

# Using npm

npm install --save @sentry/react @sentry/tracing
Next, import and initialize the Sentry module as early as possible, before initializing React:

import React from "react";
import ReactDOM from "react-dom";
import \* as Sentry from "@sentry/react";
import { Integrations } from "@sentry/tracing";
import App from "./App";

Sentry.init({
dsn: "https://32fecbc1e95048a1955262b6b297853a@o517442.ingest.sentry.io/5625266",
integrations: [new Integrations.BrowserTracing()],

// We recommend adjusting this value in production, or using tracesSampler
// for finer control
tracesSampleRate: 1.0,
});

ReactDOM.render(<App />, document.getElementById("root"));

// Can also use with React Concurrent Mode
// ReactDOM.createRoot(document.getElementById('root')).render(<App />);
