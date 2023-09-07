Future Directions
=================

Things that aren't currently supported, but are probably worth diving into in the future.


Deployment
----------

https://docs.bokeh.org/en/latest/docs/user_guide/server/deploy.html seems to be a good place to start. I haven't checked anything beyond this ;)


Development
-----------

Below are a few possible development directions, roughly sorted by descending problem size, then by importance:

- **Extension of interface to use Advanced scores as well.** Currently the interface only supports the Core scores; the Advanced scores are more numerous, more sparse (lots of NaNs are common), have more subtleties (e.g. controversy scores are "lower means better" while in general other scores are "higher means better"), and in general are just a lot more headache to deal with. It's useful to have them on this interface, but I think using the Refinitiv interface to check out Advanced scores could be the more efficient solution.
- **Denormalizing Advanced scores.** With reference to the above point: some advanced scores are presented as a percentage; these are usually already normalized with respect to the buzz of the asset (not 100% sure, please double-check the Refinitiv whitepaper). To compare their value along a time series, you would need to denormalize these scores using their corresponding buzz on each day by multiplying them together. This is NOT currently supported on the Refinitiv interface.
- **Local caching of API query results.** Currently API queries are the bottleneck limiting loading speed (becomes more obvious if you want to graph, say, 5 years of data), while also throttling some functionalities (e.g. maximum time range limit for a single query). Rewriting this interface to use locally cached data instead could solve the problem, but it will probably be a LOT of work (setting up local storage, downloading past data, parsing interface requests into corresponding filenames).
- **Error indicator.** Currently relying on terminal for error messages; surely we need them on the frontend if the Dashboard is to be deployed?
- **Scope of colors.** Different variables have different ranges; the color on the heatmap should be able to reflect that and change according to the exact types of variable on display. This is currently not supported; I've put in a range of [-50, 50] for score changes and [-5, 5] for standard deviations. Ideally it should customize to the exact dataset?
- **Extend time range of API query as appropriate.** This mainly applies to timeseries with need to calculate historical averages; there's only a historical average when there's a history, so for the first data points no such averages are calculated. If the API query is extended to fetch more historical data, this can be solved.
- **Missing data indicator.** Data sparsity causes problems; would probably be better to show how much data is missing on the interface. Currently, the rendering modules silently eats away the problem by pretending nothing's ever happened when over half of the required data points are present, or it throws a NaN and there's no middle ground.

I've also littered the source file with :code:`TODO`; some of them might make sense (implying that some of them don't). Feel free to also check that out!
