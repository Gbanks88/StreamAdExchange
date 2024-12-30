"use strict";(self.webpackChunkgrafana=self.webpackChunkgrafana||[]).push([[7680],{"./public/app/features/alerting/unified/Admin.tsx":(e,a,r)=>{r.r(a),r.d(a,{default:()=>U});var n,t=r("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/index.js"),s=r("./public/app/features/alerting/unified/components/AlertingPageWrapper.tsx"),i=r("./.yarn/__virtual__/@emotion-css-virtual-72c314ddb1/3/opt/drone/yarncache/@emotion-css-npm-11.7.1-25ff8755a7-ac1f56656f.zip/node_modules/@emotion/css/dist/emotion-css.esm.js"),l=r("./.yarn/__virtual__/react-redux-virtual-7ad20a440e/3/opt/drone/yarncache/react-redux-npm-7.2.6-134f5ed64d-0bf142ce0d.zip/node_modules/react-redux/es/index.js"),o=r("./packages/grafana-ui/src/index.ts"),c=r("./public/app/features/alerting/unified/hooks/useAlertManagerSourceName.ts"),d=r("./public/app/features/alerting/unified/hooks/useAlertManagerSources.ts"),u=r("./public/app/features/alerting/unified/hooks/useUnifiedAlertingSelector.ts"),p=r("./public/app/features/alerting/unified/state/actions.ts"),m=r("./public/app/features/alerting/unified/utils/datasource.ts"),g=r("./public/app/features/alerting/unified/utils/redux.ts"),f=r("./public/app/features/alerting/unified/components/AlertManagerPicker.tsx"),h=r("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/jsx-runtime.js");function x(){var e;const a=(0,l.useDispatch)(),r=(0,d.k)("notification"),[s,i]=(0,c.k)(r),[x,b]=(0,t.useState)(!1),{loading:j}=(0,u._)((e=>e.deleteAMConfig)),{loading:y}=(0,u._)((e=>e.saveAMConfig)),A=!!s&&(0,m.RY)(s),C=(0,o.useStyles2)(v),S=(0,u._)((e=>e.amConfigs)),{result:k,loading:N,error:_}=s&&S[s]||g.oq;(0,t.useEffect)((()=>{s&&a((0,p.Yh)(s))}),[s,a]);const $=()=>{s&&a((0,p.Nc)(s)),b(!1)},w=(0,t.useMemo)((()=>({configJSON:k?JSON.stringify(k,null,2):""})),[k]),I=j||N||y;return(0,h.jsxs)("div",{className:C.container,children:[(0,h.jsx)(f.P,{current:s,onChange:i,dataSources:r}),_&&!I&&(0,h.jsx)(o.Alert,{severity:"error",title:"Error loading Alertmanager configuration",children:_.message||"Unknown error."}),j&&s!==m.GC&&(n||(n=(0,h.jsx)(o.Alert,{severity:"info",title:"Resetting Alertmanager configuration",children:"It might take a while..."}))),s&&k&&(0,h.jsx)(o.Form,{defaultValues:w,onSubmit:e=>{s&&k&&a((0,p.mM)({newConfig:JSON.parse(e.configJSON),oldConfig:k,alertManagerSourceName:s,successMessage:"Alertmanager configuration updated.",refetch:!0}))},children:a=>{var r;let{register:n,errors:t}=a;return(0,h.jsxs)(h.Fragment,{children:[!A&&(0,h.jsx)(o.Field,{disabled:I,label:"Configuration",invalid:!!t.configJSON,error:null===(r=t.configJSON)||void 0===r?void 0:r.message,children:(0,h.jsx)(o.TextArea,Object.assign({},n("configJSON",{required:{value:!0,message:"Required."},validate:e=>{try{return JSON.parse(e),!0}catch(e){return e.message}}}),{id:"configuration",rows:25}))}),A&&(0,h.jsx)(o.Field,{label:"Configuration",children:(0,h.jsx)("pre",{"data-testid":"readonly-config",children:w.configJSON})}),!A&&(0,h.jsxs)(o.HorizontalGroup,{children:[e||(e=(0,h.jsx)(o.Button,{type:"submit",variant:"primary",disabled:I,children:"Save"})),(0,h.jsx)(o.Button,{type:"button",disabled:I,variant:"destructive",onClick:()=>b(!0),children:"Reset configuration"})]}),!!x&&(0,h.jsx)(o.ConfirmModal,{isOpen:!0,title:"Reset Alertmanager configuration",body:`Are you sure you want to reset configuration ${s===m.GC?"for the Grafana Alertmanager":`for "${s}"`}? Contact points and notification policies will be reset to their defaults.`,confirmText:"Yes, reset configuration",onConfirm:$,onDismiss:()=>b(!1)})]})}},w.configJSON)]})}const v=e=>({container:i.css`
    margin-bottom: ${e.spacing(4)};
  `});var b=r("./public/app/core/components/EmptyListCTA/EmptyListCTA.tsx");const j=/\/api\/v[1|2]\/alerts/i;var y,A;const C=e=>{let{alertmanagers:a,onChangeAlertmanagerConfig:r,onClose:n}=e;const s=(0,o.useStyles2)(S),i=(0,t.useMemo)((()=>({alertmanagers:a})),[a]),l=(0,h.jsxs)("div",{className:s.modalTitle,children:[(0,h.jsx)(o.Icon,{name:"bell",className:s.modalIcon}),y||(y=(0,h.jsx)("h3",{children:"Add Alertmanager"}))]}),c=e=>{r(e.alertmanagers.map((e=>e.url.replace(/\/$/,"").replace(/\/api\/v[1|2]\/alerts/i,"")))),n()};return(0,h.jsxs)(o.Modal,{title:l,isOpen:!0,onDismiss:n,className:s.modal,children:[(0,h.jsx)("div",{className:s.description,children:"We use a service discovery method to find existing Alertmanagers for a given URL."}),(0,h.jsx)(o.Form,{onSubmit:c,defaultValues:i,children:e=>{let{register:a,control:r,errors:n}=e;return(0,h.jsxs)("div",{children:[(0,h.jsx)(o.FieldArray,{control:r,name:"alertmanagers",children:e=>{let{fields:r,append:t,remove:i}=e;return(0,h.jsxs)("div",{className:s.fieldArray,children:[(0,h.jsx)("div",{className:s.bold,children:"Source url"}),(0,h.jsx)("div",{className:s.muted,children:"Authentication can be done via URL (e.g. user:password@myalertmanager.com) and only the Alertmanager v2 API is supported. The suffix is added internally, there is no need to specify it."}),r.map(((e,r)=>{var t;return(0,h.jsx)(o.Field,{invalid:!(null==n||null===(t=n.alertmanagers)||void 0===t||!t[r]),error:"Field is required",children:(0,h.jsx)(o.Input,Object.assign({className:s.input,defaultValue:e.url},a(`alertmanagers.${r}.url`,{required:!0}),{placeholder:"http://localhost:9093",addonAfter:(0,h.jsx)(o.Button,{"aria-label":"Remove alertmanager",type:"button",onClick:()=>i(r),variant:"destructive",className:s.destroyInputRow,children:A||(A=(0,h.jsx)(o.Icon,{name:"trash-alt"}))})}))},`${e.id}-${r}`)})),(0,h.jsx)(o.Button,{type:"button",variant:"secondary",onClick:()=>t({url:""}),children:"Add URL"})]})}}),(0,h.jsx)("div",{children:(0,h.jsx)(o.Button,{onSubmit:()=>c,children:"Add Alertmanagers"})})]})}})]})};const S=e=>{const a=i.css`
    color: ${e.colors.text.secondary};
  `;return{description:(0,i.cx)(i.css`
        margin-bottom: ${e.spacing(2)};
      `,a),muted:a,bold:i.css`
      font-weight: ${e.typography.fontWeightBold};
    `,modal:i.css``,modalIcon:(0,i.cx)(a,i.css`
        margin-right: ${e.spacing(1)};
      `),modalTitle:i.css`
      display: flex;
    `,input:i.css`
      margin-bottom: ${e.spacing(1)};
      margin-right: ${e.spacing(1)};
    `,inputRow:i.css`
      display: flex;
    `,destroyInputRow:i.css`
      padding: ${e.spacing(1)};
    `,fieldArray:i.css`
      margin-bottom: ${e.spacing(4)};
    `}};var k,N,_,$,w,I;const M=[{value:"internal",label:"Only Internal"},{value:"external",label:"Only External"},{value:"all",label:"Both internal and external"}],O=()=>{var e;const a=(0,o.useStyles2)(R),r=(0,l.useDispatch)(),[n,s]=(0,t.useState)({open:!1,payload:[{url:""}]}),[c,d]=(0,t.useState)({open:!1,index:0}),u=function(){const e=(0,l.useSelector)((e=>{var a;return null===(a=e.unifiedAlerting.externalAlertmanagers.discoveredAlertmanagers.result)||void 0===a?void 0:a.data})),a=(0,l.useSelector)((e=>{var a;return null===(a=e.unifiedAlerting.externalAlertmanagers.alertmanagerConfig.result)||void 0===a?void 0:a.alertmanagers}));if(!e||!a)return[];const r=[],n=null==e?void 0:e.droppedAlertManagers.map((e=>({url:e.url.replace(j,""),status:"dropped",actualUrl:e.url})));for(const n of a)if(0===e.activeAlertManagers.length)r.push({url:n,status:"pending",actualUrl:""});else{let a=!1;for(const t of e.activeAlertManagers)t.url===`${n}/api/v2/alerts`&&(a=!0,r.push({url:t.url.replace(j,""),status:"active",actualUrl:t.url}));a||r.push({url:n,status:"pending",actualUrl:""})}return[...r,...n]}(),m=(0,l.useSelector)((e=>{var a;return null===(a=e.unifiedAlerting.externalAlertmanagers.alertmanagerConfig.result)||void 0===a?void 0:a.alertmanagersChoice})),g=(0,o.useTheme2)();(0,t.useEffect)((()=>{r((0,p.zy)()),r((0,p.wE)());const e=setInterval((()=>r((0,p.zy)())),5e3);return()=>{clearInterval(e)}}),[r]);const f=(0,t.useCallback)((e=>{const a=(null!=u?u:[]).filter(((a,r)=>r!==e)).map((e=>e.url));r((0,p.sx)({alertmanagers:a,alertmanagersChoice:null!=m?m:"all"})),d({open:!1,index:0})}),[u,r,m]),x=(0,t.useCallback)((()=>{const e=u?[...u]:[{url:""}];s((a=>Object.assign({},a,{open:!0,payload:e})))}),[s,u]),v=(0,t.useCallback)((()=>{s((e=>{const a=u?[...u,{url:""}]:[{url:""}];return Object.assign({},e,{open:!0,payload:a})}))}),[u]),y=(0,t.useCallback)((()=>{s((e=>Object.assign({},e,{open:!1})))}),[s]),A=e=>{switch(e){case"active":return g.colors.success.main;case"pending":return g.colors.warning.main;default:return g.colors.error.main}},S=0===(null==u?void 0:u.length);return(0,h.jsxs)("div",{children:[k||(k=(0,h.jsx)("h4",{children:"External Alertmanagers"})),(0,h.jsx)("div",{className:a.muted,children:"You can have your Grafana managed alerts be delivered to one or many external Alertmanager(s) in addition to the internal Alertmanager by specifying their URLs below."}),(0,h.jsx)("div",{className:a.actions,children:!S&&(0,h.jsx)(o.Button,{type:"button",onClick:v,children:"Add Alertmanager"})}),S?(0,h.jsx)(b.Z,{title:"You have not added any external alertmanagers",onClick:v,buttonTitle:"Add Alertmanager",buttonIcon:"bell-slash"}):(0,h.jsxs)(h.Fragment,{children:[(0,h.jsxs)("table",{className:(0,i.cx)("filter-table form-inline filter-table--hover",a.table),children:[(0,h.jsx)("thead",{children:(0,h.jsxs)("tr",{children:[N||(N=(0,h.jsx)("th",{children:"Url"})),_||(_=(0,h.jsx)("th",{children:"Status"})),(0,h.jsx)("th",{style:{width:"2%"},children:"Action"})]})}),(0,h.jsx)("tbody",{children:null==u?void 0:u.map(((r,n)=>(0,h.jsxs)("tr",{children:[(0,h.jsxs)("td",{children:[(0,h.jsx)("span",{className:a.url,children:r.url}),r.actualUrl?(0,h.jsx)(o.Tooltip,{content:`Discovered ${r.actualUrl} from ${r.url}`,theme:"info",children:$||($=(0,h.jsx)(o.Icon,{name:"info-circle"}))}):null]}),(0,h.jsx)("td",{children:(0,h.jsx)(o.Icon,{name:"heart",style:{color:A(r.status)},title:r.status})}),(0,h.jsx)("td",{children:(0,h.jsxs)(o.HorizontalGroup,{children:[e||(e=(0,h.jsx)(o.Button,{variant:"secondary",type:"button",onClick:x,"aria-label":"Edit alertmanager",children:w||(w=(0,h.jsx)(o.Icon,{name:"pen"}))})),(0,h.jsx)(o.Button,{variant:"destructive","aria-label":"Remove alertmanager",type:"button",onClick:()=>d({open:!0,index:n}),children:I||(I=(0,h.jsx)(o.Icon,{name:"trash-alt"}))})]})})]},n)))})]}),(0,h.jsx)("div",{children:(0,h.jsx)(o.Field,{label:"Send alerts to",description:"Sets which Alertmanager will handle your alerts. Internal (Grafana built in Alertmanager), External (All Alertmanagers configured above), or both.",children:(0,h.jsx)(o.RadioButtonGroup,{options:M,value:m,onChange:e=>(e=>{r((0,p.sx)({alertmanagers:u.map((e=>e.url)),alertmanagersChoice:e}))})(e)})})})]}),(0,h.jsx)(o.ConfirmModal,{isOpen:c.open,title:"Remove Alertmanager",body:"Are you sure you want to remove this Alertmanager",confirmText:"Remove",onConfirm:()=>f(c.index),onDismiss:()=>d({open:!1,index:0})}),n.open&&(0,h.jsx)(C,{onClose:y,alertmanagers:n.payload,onChangeAlertmanagerConfig:e=>{r((0,p.sx)({alertmanagers:e,alertmanagersChoice:null!=m?m:"all"}))}})]})},R=e=>({url:i.css`
    margin-right: ${e.spacing(1)};
  `,muted:i.css`
    color: ${e.colors.text.secondary};
  `,actions:i.css`
    margin-top: ${e.spacing(2)};
    display: flex;
    justify-content: flex-end;
  `,table:i.css`
    margin-bottom: ${e.spacing(2)};
  `});var z;function U(){return z||(z=(0,h.jsxs)(s.J,{pageId:"alerting-admin",children:[(0,h.jsx)(x,{"test-id":"admin-alertmanagerconfig"}),(0,h.jsx)(O,{"test-id":"admin-externalalertmanagers"})]}))}},"./public/app/features/alerting/unified/components/AlertingPageWrapper.tsx":(e,a,r)=>{r.d(a,{J:()=>l});r("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/index.js");var n=r("./.yarn/__virtual__/react-redux-virtual-7ad20a440e/3/opt/drone/yarncache/react-redux-npm-7.2.6-134f5ed64d-0bf142ce0d.zip/node_modules/react-redux/es/index.js"),t=r("./public/app/core/components/Page/Page.tsx"),s=r("./public/app/core/selectors/navModel.ts"),i=r("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/jsx-runtime.js");const l=e=>{let{children:a,pageId:r,isLoading:l}=e;const o=(0,s.h)((0,n.useSelector)((e=>e.navIndex)),r);return(0,i.jsx)(t.Z,{navModel:o,children:(0,i.jsx)(t.Z.Contents,{isLoading:l,children:a})})}},"./public/app/features/alerting/unified/hooks/useAlertManagerSourceName.ts":(e,a,r)=>{r.d(a,{k:()=>o});var n=r("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/index.js"),t=r("./public/app/core/hooks/useQueryParams.ts"),s=r("./public/app/core/store.ts"),i=r("./public/app/features/alerting/unified/utils/constants.ts"),l=r("./public/app/features/alerting/unified/utils/datasource.ts");function o(e){const[a,r]=(0,t.K)(),o=function(e){return(0,n.useCallback)((a=>e.map((e=>e.name)).includes(a)),[e])}(e),c=(0,n.useCallback)((e=>{o(e)&&(e===l.GC?(s.Z.delete(i.de),r({[i.c4]:null})):(s.Z.set(i.de,e),r({[i.c4]:e})))}),[r,o]),d=a[i.c4];if(d&&"string"==typeof d)return o(d)?[d,c]:[void 0,c];const u=s.Z.get(i.de);return u&&"string"==typeof u&&o(u)?(c(u),[u,c]):o(l.GC)?[l.GC,c]:[void 0,c]}},"./public/app/features/alerting/unified/hooks/useAlertManagerSources.ts":(e,a,r)=>{r.d(a,{k:()=>s});var n=r("../../opt/drone/yarncache/react-npm-17.0.2-99ba37d931-b254cc17ce.zip/node_modules/react/index.js"),t=r("./public/app/features/alerting/unified/utils/datasource.ts");function s(e){return(0,n.useMemo)((()=>(0,t.LE)(e)),[e])}}}]);
//# sourceMappingURL=AlertingAdmin.0dfd49f78dc93c695e30.js.map