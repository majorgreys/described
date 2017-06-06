import * as React from "react";
import { Field, reduxForm } from 'redux-form';
import { InputGroup } from "@blueprintjs/core";

export interface ItemProps {
    id: string;
    title: string;
}

export class Item extends React.Component<ItemProps, undefined> {
    render() {
        return (
            <div>
                <label className="pt-label .pt-inline">
                    Document Type
                    <div className="pt-select">
                        <select>
                            <option selected>Select...</option>
                            <option value="1">Newspaper Article</option>
                            <option value="2">Journal Article</option>
                            <option value="3">Manuscript</option>
                            <option value="4">Letter</option>
                        </select>
                    </div>
                </label>
                <label className="pt-label .pt-inline">
                    Title 
                    <input className="pt-input" type="text" placeholder="Input title" dir="auto" />
                </label>
            </div>
        );
    }
}