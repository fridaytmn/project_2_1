SCRIPT_GOOGLETAGMANAGER = """
<!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-V9JNY5BF6K">
    </script>
    <script>   window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}   gtag('js', new Date());
    gtag('config', 'G-V9JNY5BF6K');
    </script>
    """

SCRIPT_OKO = r"""
<script>
((win, doc, script) => {
  const oko = win.oko instanceof Array ? win.oko : [];
  const host = oko.host || 'oko.sima-land.ru';
  const screen = win.screen;

  /**
   * Отправляет событие в ОКО
   */
  oko.push = (event, modifiedInfo = {}) => {
    if(!event) return;

    /**
     * Объект с информацией о собыии
     */
    const info = oko.info || {
      ...oko?.defaultsAll,
      vp: [screen.availWidth, screen.availHeight],
      sr: [screen.width, screen.height],
      "ya-uid": (doc.cookie.match(/_ym_uid=([0-9]+)/) ?? [])[1],
      "ga-uid": (doc.cookie.match(/GA[\d.]+/) ?? [])[0],
      ref: doc.referrer,
      'full-url-path': win.location.pathname,
    }

    const {
      n: eventName = '',
      'source-id': sourceId = 1,
      ...eventData
    } = event;

    const encode = encodeURIComponent;

    let src = `//${host}/watch.js?`;
    src += 'v=6';
    src += `&t=${Date.now()}`;
    src += `&n=${eventName}`;
    src += `&d=${encode(JSON.stringify(eventData))}`;
    src += `&source-id=${sourceId}`;
    src += `&i=${encode(JSON.stringify({
      ...info,
      ...modifiedInfo,
    }))}`;

    const scriptElement = doc.createElement(script);
    const firstScriptTag = doc.querySelector('script');

    scriptElement.async = true;
    scriptElement.src = src;
    scriptElement.referrerPolicy = 'no-referrer-when-downgrade';

    firstScriptTag.parentNode.insertBefore(scriptElement, firstScriptTag);
  };

  /**
   * При иницилизации скрипта отправляем пустое событие
   */
  oko.push({});

  win.history.pushState = new Proxy(window.history.pushState, {
    apply: (target, thisArg, argArray) => {
      oko.push({}, {
        ref: win.location.href,
        'full-url-path': argArray[2],
      })
      return target.apply(thisArg, argArray);
    },
  });

  win.oko = oko;

})(window, document, 'script');


</script>
"""

INDEX_STRING = (
    """<!DOCTYPE html>
<html>
    <head>
    """
    + SCRIPT_GOOGLETAGMANAGER
    + SCRIPT_OKO
    + """
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""
)
