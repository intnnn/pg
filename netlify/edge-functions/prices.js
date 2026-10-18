import worker from "../../worker/index.js";

export default async function prices(request) {
  return worker.fetch(request);
}
