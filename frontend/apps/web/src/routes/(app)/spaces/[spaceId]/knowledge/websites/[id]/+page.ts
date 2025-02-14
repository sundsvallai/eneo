export const load = async (event) => {
  const { intric } = await event.parent();

  event.depends("crawlruns:list");

  const [website, crawlRuns, infoBlobs] = await Promise.all([
    intric.websites.get({ id: event.params.id }),
    intric.websites.crawlRuns.list({ id: event.params.id }),
    intric.websites.indexedBlobs.list({ id: event.params.id })
  ]);

  return {
    crawlRuns: crawlRuns.reverse(),
    infoBlobs,
    website
  };
};
