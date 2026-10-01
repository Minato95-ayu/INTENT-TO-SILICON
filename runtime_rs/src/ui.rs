use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Style {
    pub display: String,
    pub flex_direction: String,
    pub justify_content: String,
    pub align_items: String,
    pub padding: String,
    pub margin: String,
    pub width: String,
    pub height: String,
    pub background_color: String,
    pub color: String,
}

impl Default for Style {
    fn default() -> Self {
        Self {
            display: "block".to_string(),
            flex_direction: "row".to_string(),
            justify_content: "flex-start".to_string(),
            align_items: "stretch".to_string(),
            padding: "0".to_string(),
            margin: "0".to_string(),
            width: "auto".to_string(),
            height: "auto".to_string(),
            background_color: "transparent".to_string(),
            color: "inherit".to_string(),
        }
    }
}

impl Style {
    pub fn to_css(&self) -> String {
        format!(
            "display: {}; flex-direction: {}; justify-content: {}; align-items: {}; padding: {}; margin: {}; width: {}; height: {}; background-color: {}; color: {};",
            self.display, self.flex_direction, self.justify_content, self.align_items,
            self.padding, self.margin, self.width, self.height, self.background_color, self.color
        )
    }
}

pub struct UiNode {
    pub tag: String,
    pub children: Vec<UiNode>,
    pub props: HashMap<String, String>,
    pub style: Option<Style>,
    pub text_content: Option<String>,
}

impl UiNode {
    pub fn new(tag: &str) -> Self {
        Self {
            tag: tag.to_string(),
            children: Vec::new(),
            props: HashMap::new(),
            style: None,
            text_content: None,
        }
    }

    pub fn with_style(mut self, style: Style) -> Self {
        self.style = Some(style);
        self
    }

    pub fn with_text(mut self, text: &str) -> Self {
        self.text_content = Some(text.to_string());
        self
    }

    pub fn add_child(mut self, child: UiNode) -> Self {
        self.children.push(child);
        self
    }

    pub fn render(&self) -> String {
        let mut props_str = String::new();
        for (k, v) in &self.props {
            props_str.push_str(&format!(" {}=\"{}\"", k, v));
        }
        if let Some(style) = &self.style {
            props_str.push_str(&format!(" style=\"{}\"", style.to_css()));
        }
        
        let content = if let Some(text) = &self.text_content {
            text.clone()
        } else {
            let mut children_str = String::new();
            for child in &self.children {
                children_str.push_str(&child.render());
            }
            children_str
        };

        if content.is_empty() && self.children.is_empty() {
            format!("<{}{} />", self.tag, props_str)
        } else {
            format!("<{}{}>{}</{}>", self.tag, props_str, content, self.tag)
        }
    }
}
