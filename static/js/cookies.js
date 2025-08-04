var COOKIES = COOKIES || {
  /*
     指定したcookieの値を取得して返す関数
     第1引数=取得したいcookiename
    */
  getCookie: function (cName, defaultValue = null) {
    var cookie_name = cName;
    if (cookie_name == "" || cookie_name == null) {
      console.log("COOKIES.getCookie：引数に値を代入してください。");
    } else {
      var set_replace = "(?:(?:^|.*s*)" + cookie_name + "s*=s*([^;]*).*$)|^.*$";
      var cookie_value = document.cookie.replace(new RegExp(set_replace), "$1");
      return cookie_value || defaultValue;
    }
  },
  /*
     指定したcookieを追加する関数
     第1引数=追加するcookiename;第2引数=追加するcookievalue;第3引数=cookieの有効期限(day)
    */
  setCookie: function (cName, cValue, cTime) {
    var cookie_name = cName;
    var cookie_Value = cValue;
    var cookie_domain = location.hostname;
    var cookie_time = cTime ? 60 * 60 * 24 * cTime : "";
    if (cookie_name == "" || cookie_name == null) {
      console.log("COOKIES.setCookie：第1引数に値を代入してください。");
    } else {
      document.cookie = cookie_name + "=" + cookie_Value + ";domain=" + cookie_domain + ";max-age=" + cookie_time;
    }
  },
  /*
     指定したcookieの値を削除する関数
     第1引数=削除したいcookiename
    */
  deleteCookie: function (cName) {
    var cookie_name = cName;
    if (cookie_name == "" || cookie_name == null) {
      console.log("COOKIES.deleteCookie：引数に値を代入してください。");
    } else {
      COOKIES.setCookie(cookie_name, "", 0);
    }
  },
};
