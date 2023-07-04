window.onload = function () {
  const terminal = new Terminal({
    cursorBlink: "block",
    fontSize: 12,
  });
  terminal.attachCustomKeyEventHandler(customKeyEventHandler);
  f = new FitAddon.FitAddon();
  terminal.loadAddon(f);
  const container = document.getElementById("terminal-container");
  terminal.open(container);
  f.fit();
  var process;
  new QWebChannel(qt.webChannelTransport, function (channel) {
    process = channel.objects.process;
    var resize_listener = channel.objects.resize_listener;
    var open_browser_url = channel.objects.open_browser_url;
    terminal.onKey(function (e) {
      // console.error("Pressing key "+e.key.charCodeAt(0))
      if (e.key.charCodeAt(0) == 13) {
        process.send_data("\n");
      } else {
        process.send_data(e.key);
      }
    });
    process.data_changed.connect(function (text) {
      terminal.write(text);
    });
    resize_listener.resized.connect(function () {
      f.fit();
    });
    terminal.loadAddon(
      new WebLinksAddon.WebLinksAddon(function (e, uri) {
        // console.error(uri);
        open_browser_url.open(uri);
      })
    );
  });

  function customKeyEventHandler(e) {
    if (e.type !== "keydown") {
      return true;
    }
    if (e.ctrlKey && e.shiftKey) {
      const key = e.key.toLowerCase();
      if (key === "v") {
        // ctrl+shift+v: paste whatever is in the clipboard
        navigator.clipboard.readText().then((toPaste) => {
          process.send_data(toPaste);
        });
        return false;
      } else if (key === "c" || key === "x") {
        // ctrl+shift+x: copy whatever is highlighted to clipboard

        // 'x' is used as an alternate to 'c' because ctrl+c is taken
        // by the terminal (SIGINT) and ctrl+shift+c is taken by the browser
        // (open devtools).
        // I'm not aware of ctrl+shift+x being used by anything in the terminal
        // or browser
        const toCopy = terminal.getSelection();
        navigator.clipboard.writeText(toCopy);
        terminal.focus();
        return false;
      }
    }
    return true;
  }
};
